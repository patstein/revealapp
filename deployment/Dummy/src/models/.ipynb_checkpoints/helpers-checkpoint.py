import pandas as pd
import numpy as np
import logging
import os
import scipy
import csv
import gzip
import math
from datetime import datetime

import nltk
from nltk import PunktSentenceTokenizer

import torch
from torch.utils.data import DataLoader

from sentence_transformers import models, losses
from sentence_transformers import SentencesDataset, LoggingHandler, SentenceTransformer, losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from sentence_transformers.readers import STSDataReader, LabelSentenceReader, InputExample

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier, LinearRegression, LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_auc_score, roc_curve, mean_squared_error






class DFReader:
    
    """
    Reads data for active learning. Each line contains two sentences (s1_col_idx, s2_col_idx) and one label (score_col_idx)    
    """
    
    def __init__(self, s1_col_idx=1, s2_col_idx=2, score_col_idx=0):

        self.score_col_idx = score_col_idx
        self.s1_col_idx = s1_col_idx
        self.s2_col_idx = s2_col_idx

    def get_examples(self, df, max_examples=0):
                
        examples = []
        for id, row in df.iterrows():
            score = float(row[self.score_col_idx])
            s1 = row[self.s1_col_idx]
            s2 = row[self.s2_col_idx]
            examples.append(InputExample(guid='temp_df'+str(id), texts=[s1, s2], label=score))

        return examples





def split_in_sentences (DocRow):
    
    '''
    Converts a df row of raw text documents with DocID into a sentence df that is compatible with tags df
    '''
    
    PunktTokenizer = PunktSentenceTokenizer().span_tokenize(DocRow['FullText'])
    sent_intervals = [interval for interval in PunktTokenizer]    #returns start and end index for each sentence
    text_splitted = [DocRow['FullText'][index_tuple[0]:index_tuple[1]] for index_tuple in sent_intervals]
    
    starts  = [interval[0] for interval in sent_intervals]
    ends    = [interval[1] for interval in sent_intervals]
    lengths = [end - end_before for (end, end_before) in zip(ends[1:] , ends[:-1])]
    lengths.insert(0,ends[0])
    
    for idx, length in enumerate(lengths[:-1]):
        starts[idx+1] = starts[idx] + length 
            
    df_Sentences = pd.DataFrame({
                             'DocID': DocRow['DocID'],
                             'SentID': range(len(text_splitted)),
                             'SentText': text_splitted,
                             'SentStartIdx': starts,
                             'SentLength': lengths                            
                            })    
    
    return df_Sentences





def get_tag_sentence (TagRow, Sentences):
    
    '''
    Returns the corresponding text to a tag row in the UserTags / SugestedTags data
    '''

    SentenceRow = Sentences[
        (Sentences['DocID'] == TagRow['DocID']) & 
        (Sentences['SentStartIdx'] <= TagRow['TagStartIdx']) &
        (Sentences['SentStartIdx'] + Sentences['SentLength'] > TagRow['TagStartIdx'])
    ]

    return SentenceRow['SentText'].values[0] 





def suggest_most_similar_cosine (TagRow,sentences_embeddings, df_UserTags, df_Sentences, model, top_n):
    
    '''
    Returns a df of sentences most similar to a tag
    '''
    
    TagEmbedding = pd.DataFrame(model.encode([TagRow['TagText']]))
    Suggestions = df_Sentences
    
    Suggestions['SimilarityScore'] = cosine_similarity(TagEmbedding, sentences_embeddings).T
    Suggestions['TagID'] = TagRow['TagID']
    Suggestions['TagAccepted'] = None
    
    Suggestions = Suggestions.sort_values(
        by = 'SimilarityScore', 
        ascending = False).iloc[0:top_n,:]
    
    Suggestions['TagAccepted'].iloc[0] = 1.0 # the firs one is the tagged sentence itself, which is user-defined
    
    return(Suggestions)





def get_training_pairs (RowSuggestion, df_Suggestions, df_UserTags):

    '''
    Returns a df of annotated sentence pairs based on the user tags and evaluations
    '''
    
    Suggestions = df_Suggestions[
                    (df_Suggestions['TagID'] == RowSuggestion['TagID']) & 
                    (df_Suggestions['SuggestionID'] != RowSuggestion['SuggestionID'])]

    Suggestions['SentCompareText'] = RowSuggestion['SentText']
    TrainPairs = Suggestions.loc[:,['Accepted','SentText', 'SentCompareText']].dropna()  

    return TrainPairs





def get_train_loader (df, batch, epoch, model):
    
    '''
    prepare data for active learning
    '''
    
    logging.info("Read active learning dataset")
    train_data = SentencesDataset(examples = DFReader().get_examples(df), model = model)
    train_dataloader = DataLoader(train_data, shuffle=True, batch_size = batch)
    train_loss = losses.CosineSimilarityLoss(model=model)

    # Configure the training warmup
    warmup_steps = math.ceil(len(train_data)*epoch/batch*0.1) #10% of train data for warm-up
    logging.info("Warmup-steps: {}".format(warmup_steps))

    return train_dataloader, train_loss, warmup_steps





def get_evaluator (df, batch, model):
    
    '''
    prepare data for active learning evaluation 
    evaluation is not used but neccessary to run the training
    '''
    
    logging.info("Read evaluation dataset")
    eval_data = SentencesDataset(examples = DFReader().get_examples(df, max_examples = 10), model = model) # converts to embedding
    eval_dataloader = DataLoader(eval_data, shuffle=False, batch_size = batch)
    evaluator = EmbeddingSimilarityEvaluator(eval_dataloader) 

    return eval_dataloader, evaluator





def train_active(df_train, df_eval, model):
    
    '''
    define training parameters
    '''
    
    train_batch_size = 128 # Where does this belong?
    num_epochs = 4 # Where does this belong?
    train_dataloader, loss, warmup_steps = get_train_loader(df_train, train_batch_size, num_epochs, model)
    eval_dataloader, evaluator = get_evaluator(df_eval, train_batch_size, model)
    
  
    '''
    do the training:
    '''
    
    model.fit(train_objectives=[(train_dataloader, loss)],
          evaluator = evaluator,
          epochs = num_epochs,
          evaluation_steps = 100,
          warmup_steps = warmup_steps,
          #output_path=model_save_path # will use save below in order to overwrite
         )
    
    return model
### ---------------------------------------------------------------
### THIS FILE CONTAINS ALL THE MODULES FOR THE API 
### ---------------------------------------------------------------


    
'''
load the packages that are neccessary to run the model: (might contain excess)
'''

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



from helpers import *
    
    




    
'''
Uncomment part marked with #ACTIVATE for Server
these are the paths used to save and colllect documents and models
'''

MODEL_PRETRAINED = 'bert-base-nli-mean-tokens'

BlockID = ''
path_base = '/home/sevi/revealStorage/'
# path_base = '../'

path_model_pretrained = path_base + 'models/pretrained/' #+ MODEL_PRETRAINED
path_model_adapted = path_base + 'models/adapted/model' #+ str(BlockID)

path_documents = path_base + 'data/raw/documents' #+ str(BlockID)
path_sentences = path_base + 'data/sentences/sentences' #+ str(BlockID)
path_embeddings = path_base + 'data/embeddings/embeddings' #+ str(BlockID)

path_tags = path_base + 'data/tags_user/tags_user' #+ str(BlockID)
path_tags_suggested = path_base + 'data/tags_suggested/tags_suggested' #+ str(BlockID)

folders_to_be_created = [
      path_model_pretrained
    , path_model_adapted[:-(path_model_adapted[::-1].find('/'))]
    , path_documents[:-(path_documents[::-1].find('/'))]
    , path_sentences[:-(path_sentences[::-1].find('/'))]
    , path_embeddings[:-(path_embeddings[::-1].find('/'))]
    , path_tags[:-(path_tags[::-1].find('/'))]
    , path_tags_suggested[:-(path_tags_suggested[::-1].find('/'))]
]

#ACTIVATE for Server
#create folder structure if not exists:
# for directory in folders_to_be_created:
#     if not os.path.exists(directory):
#         os.makedirs(directory)
# os.chown(path_base, SERVER_USER_ID, SERVER_USER_ID)
# for root, dirs, files in os.walk(path_base):   #set ownership of folder (and all subfolders) to root account
#     for momo in dirs:  
#         os.chown(os.path.join(root, momo), SERVER_USER_ID, SERVER_USER_ID)


    
    
    
    
    


def process_documents (DocumentsRaw, BlockID = 0):    
    
    
    '''
    Tthis function: 
        generates a sentences dataframe from the raw documents
        initiates a model with the BlockID (it can be trained further on new documents later)
        generates embeddings for all sentences
        saves model, text and sentence data and the embeddings for further use
    Returns:
        None       
    Arguments:
        DocumentsRaw: a dict of raw text strings and their IDs (from json)
        BlockID: an ID to identify data and model that belong together (default=0; all texts and tags work whith one model) 
        AdaptModel = False: adapting the embeddings to the text (not available at the moment) 
        
    '''
       
    
    # convert the input:     
    df_DocumentsRaw = pd.DataFrame(
        data = DocumentsRaw, 
        columns = ['DocID','FullText'])     
    
        
    # generate the sentences dataframe from documents:    
    df_Sentences = pd.concat(list(
        df_DocumentsRaw.apply(
            split_in_sentences, 
            axis = 1)))  
     

    # initiate a copy of the pretrained model:      
    model = SentenceTransformer(MODEL_PRETRAINED)   
    
        
    # create embeddings:    
    corpus = list(df_Sentences['SentText']) 
    df_Embeddings = pd.DataFrame(model.encode(corpus))    
    df_Embeddings.index = df_Sentences.index.values 


    # save data for further training and evaluation:    
    df_DocumentsRaw.to_csv(path_documents + str(BlockID) + '.csv')
    df_Sentences.to_csv(path_sentences + str(BlockID) + '.csv')
    df_Embeddings.to_csv(path_embeddings + str(BlockID) + '.csv')


    # save model for further training and evaluation:    
    model.save(path_model_adapted + str(BlockID))  


    return None 
    # currently, this function does not return anything  
 
    
    
    
    
    
    
    

def suggest_similars (UserTags, BlockID=0, top_n = 10):
    
    
    '''
    This function: 
        finds the closest sentences for each UserTag, using the pretrained model and the documents uploaded to the block
        saves tags and tags suggestions
    Returns:
        a dataframe of suggested tags whith their suggestion sterngth       
    Arguments: 
        UserTags: a table whith tags and parameters of the text belonging them
        BlockID: an ID to identify data and model that belong together (default=0; all texts and tags work whith one model) 
        top_n: the number of desired suggestions 
        
    '''
        
    # convert the input:    
    df_UserTags = pd.DataFrame(UserTags)
    df_UserTags.columns = 'TagID', 'DocID', 'TagStartIdx', 'TagLength' 
    
        
    # collect the initiated and trained (if already) model:    
    model = SentenceTransformer(path_model_adapted + str(BlockID))   
    model.eval() # put model into evaluation mode - should not be neccessary
    
        
    # collect the previously processed sentences and embeddings:    
    df_Sentences = pd.read_csv(path_sentences + str(BlockID) + '.csv')
    df_Embeddings = pd.read_csv(path_embeddings + str(BlockID) + '.csv')
    
    
    # find the sentences corresponding the tags:    
    df_UserTags['TagText'] = df_UserTags.apply(get_tag_sentence, args = [df_Sentences], axis = 1)

        
    # create embeddings for the sentences:    
    corpus_sentences = list(df_Sentences['SentText'])
    df_EmbeddingsSent = pd.DataFrame(model.encode(corpus_sentences))    
    df_EmbeddingsSent.index = df_Sentences.index.values    
    

    # generate embeddings for tags for the comparison:    
    corpus_tags = list(df_UserTags['TagText'])
    df_EmbeddingsTags = pd.DataFrame(model.encode(corpus_tags))
    df_EmbeddingsTags.index = df_UserTags.index.values    
    
 
    # generate tag suggestions for each tag:    
    df_TagSuggestions = pd.concat(list(
        df_UserTags.apply(
            suggest_most_similar_cosine, 
            args = [df_EmbeddingsSent, 
                    df_UserTags, 
                    df_Sentences, 
                    model, 
                    top_n], 
            axis = 1)))
      
    
    # save data for further training and evaluation:    
    df_UserTags.to_csv(path_tags + str(BlockID) + '.csv')
    df_TagSuggestions.to_csv(path_tags_suggested + str(BlockID) + '.csv')
    
        
    return df_TagSuggestions
    # this has to be translated to json

    
    
    





def learn_suggest (TagSuggestions, BlockID=0, top_n = 10 ):
    
    
    '''
    This function:
        actualises (trains) the initialised pretrained model, based on user-generated tags and tag evaluations
        finds the closest sentences for each UserTag, using the actualised model and the documents uploaded to the block
        saves actualised model, tags and tags suggestions   
    Returns:
        a dataframe of suggested tags whith their suggestion sterngth    
    Arguments: 
        TagSuggestions: a table whith previous tag suggestions evaluated by user
        BlockID: an ID to identify data and model that belong together (default=0; all texts and tags work whith one model) 
        top_n: the number of desired new suggestions 
        
    '''
     
        
    # convert the input:    
    df_TagSuggestions = pd.DataFrame(TagSuggestions)
    df_TagSuggestions.columns = 'SuggestionID', 'DocID', 'TagStartIdx', 'TagLength', 'TagID', 'SimilarityScore', 'Accepted'
    
        
    # collect the initiated and trained (if already) model:    
    model = SentenceTransformer(path_model_adapted + str(BlockID))   
    model.eval() # put model into evaluation mode - should not be neccessary
        
    
    # collect the previously processed sentences an, tags and embeddings:    
    df_Sentences = pd.read_csv(path_sentences + str(BlockID) + '.csv')    
    df_UserTags = pd.read_csv(path_tags + str(BlockID) + '.csv')
    df_Embeddings = pd.read_csv(path_embeddings + str(BlockID) + '.csv')    
        
    
    # collect the sentences corresponding the tags and suggestions:
    df_TagSuggestions['SentText'] = df_TagSuggestions.apply(
        get_tag_sentence, 
        args = [df_Sentences], 
        axis = 1)
    
    df_UserTags['TagText'] = df_UserTags.apply(
        get_tag_sentence, 
        args = [df_Sentences], 
        axis = 1)


    # create ActiveLearning sentence pairs from suggestion feedback:     
    df_LearnActive = pd.concat(list(
        df_TagSuggestions.apply(
              get_training_pairs, 
              args = [df_TagSuggestions, df_UserTags], 
              axis = 1)))

    
    # train model on the ActiveLearning sentence pairs:    
    model_trained = train_active(df_LearnActive, df_LearnActive, model)

    
    # create embeddings:    
    corpus_sentences = list(df_Sentences['SentText'])    
    df_EmbeddingsSent = pd.DataFrame(model.encode(corpus_sentences))    
    df_EmbeddingsSent.index = df_Sentences.index.values  

    corpus_suggestions = list(df_TagSuggestions['SentText'])
    df_EmbeddingsSug = pd.DataFrame(model.encode(corpus_suggestions))    
    df_EmbeddingsSug.index = df_TagSuggestions.index.values       
    
    corpus_tags = list(df_UserTags['TagText'])
    df_EmbeddingsTags = pd.DataFrame(model.encode(corpus_tags))
    df_EmbeddingsTags.index = df_UserTags.index.values    
    

    # generate tag suggestions (currently this just overwrites the recieved ones):    
    df_TagSuggestions = pd.concat(list(
        df_UserTags.apply(
            suggest_most_similar_cosine, 
            args = [df_EmbeddingsSent, 
                    df_UserTags, 
                    df_Sentences, 
                    model_trained, 
                    top_n], 
            axis = 1)))
    
    
    # save data for further training and evaluation:    
    df_TagSuggestions.to_csv(path_tags_suggested + str(BlockID) + '.csv')

    
    # save the trained model for further training and evaluation:    
    model_trained.save(path_model_adapted + str(BlockID))  

    
    return df_TagSuggestions
    # this has to be translated to json
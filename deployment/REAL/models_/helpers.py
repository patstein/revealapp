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
            examples.append(InputExample(guid='temp_df' + str(id), texts=[s1, s2], label=score))

        return examples




def update_andor_save_data(df_New, path, override=False):
    '''
    saves data or merges it with existing data if any
    '''

    if (os.path.exists(path) and not override):
        df_Old = pd.read_pickle(path)
        df_New = pd.concat([df_New, df_Old])#.drop_duplicates()

    df_New.to_pickle(path)


def split_in_sentences(DocRow):
    '''
    Converts a df row of raw text documents with DocID into a sentence df that is compatible with tags df
    '''

    PunktTokenizer = PunktSentenceTokenizer().span_tokenize(DocRow['content_text'])
    sent_intervals = [interval for interval in PunktTokenizer]  # returns start and end index for each sentence
    text_splitted = [DocRow['content_text'][index_tuple[0]:index_tuple[1]] for index_tuple in sent_intervals]

    starts = [interval[0] for interval in sent_intervals]
    ends = [interval[1] for interval in sent_intervals]
    lengths = [end - end_before for (end, end_before) in zip(ends[1:], ends[:-1])]
    lengths.insert(0, ends[0])

    for idx, length in enumerate(lengths[:-1]):
        starts[idx + 1] = starts[idx] + length

    df_Sentences = pd.DataFrame({
        'id_sent_rel': range(len(text_splitted)),
        'id_doc': DocRow['id_doc'],
        'id_user': DocRow['id_user'],
        'start_idx': starts,
        'end_idx': ends,
        'text': text_splitted,
    })

    return df_Sentences


def get_highlight_sentence(HighlightRow, Sentences):
    '''
    Returns the corresponding text to a tag row in the UserTags / SugestedTags data
    '''

    SentenceRow = Sentences[
        (Sentences['id_doc'] == HighlightRow['id_doc']) &
        (Sentences['start_idx'] <= HighlightRow['start_idx']) &
        (Sentences['end_idx'] > HighlightRow['start_idx'])
        ]

    return SentenceRow['text'].values[0], SentenceRow.index.values[0]


def suggest_most_similar_cosine(HighlightRow, Embeddings, Sentences, model, sim_threshold):
    # TODO: make this function more efficient. Especially Suggestions = Sentences will be very slow
    '''
    Returns a df of sentences most similar to a tag
    '''
    Suggestions = pd.DataFrame()

    #for each row in highlights which is either user-generated (suggested == 0) or accepted by the user (accpeted == 1) we find most similars:
    if (HighlightRow['suggested'] == 0) | (HighlightRow['accepted'] == 1):
        # calculate the embedding of the highlighted sentence
        # on purpose we don't take it from the stored embeddings because we later might wanna also search for similar to freetext
        RowEmbedding = pd.DataFrame(
            model.encode([HighlightRow['text']]))

        Suggestions = Sentences[Sentences['suggestible']].copy()
        Suggestible_Embeddings = Embeddings[Embeddings.index.isin(Suggestions['id_sent'])]
        # Suggestions = Suggestions.rename(columns = {'id_sent': 'id_highlight'})   # not working for unknown
        # reasons, so:
        Suggestions['id_highlight'] = Suggestions['id_sent']
        Suggestions.drop(['id_sent'], axis=1, inplace=True)

        Suggestions['id_tag'] = HighlightRow['id_tag']
        Suggestions['suggested'] = 1

        Suggestions['score'] = cosine_similarity(RowEmbedding, Suggestible_Embeddings).T
        Suggestions['id_parent_highlight'] = HighlightRow['id_highlight']  # or id_parent_highlight?

        Suggestions['accepted'] = None

        Suggestions['date_created'] = HighlightRow[
            'date_created']  # will we modify this ourselves, or is it just a Platzhalter?
        Suggestions['date_updated'] = HighlightRow[
            'date_updated']  # will we modify this ourselves, or is it just a Platzhalter?

        final_columns = Suggestions.columns
        Suggestions = Suggestions[Suggestions['score'] >= sim_threshold]
        #Suggestions = Suggestions.sort_values(by='score', ascending=False).iloc[0:top_n, :]

        # check if empty suggestions
        if Suggestions.empty:
            Suggestions = pd.DataFrame(columns=final_columns)

    return Suggestions


def get_training_pairs(RowHighlights, Highlights):
    '''
    Returns a df of annotated sentence pairs based on the user tags and evaluations
    '''

    Items = Highlights.loc[:, ['id_sent', 'id_tag', 'id_highlight', 'suggested', 'accepted', 'text']]

    Items['compare_to_text'] = RowHighlights['text']
    Items['y'] = Items.apply(
        (lambda x: 1 if x['suggested'] == 0 else x['accepted']),
        axis=1)

    Items = Items[(Items['id_tag'] == RowHighlights['id_tag']) &
                  (Items['id_highlight'] != RowHighlights['id_highlight'])]  # of highlights of same tag but not itself

    TrainPairs = Items.loc[:, ['y', 'text', 'compare_to_text']].dropna()

    return TrainPairs


def get_train_loader(df, batch, epoch, model):
    '''
    prepare data for active learning
    '''

    logging.info("Read active learning dataset")
    train_data = SentencesDataset(examples=DFReader().get_examples(df), model=model)
    train_dataloader = DataLoader(train_data, shuffle=True, batch_size=batch)
    train_loss = losses.CosineSimilarityLoss(model=model)
    # Configure the training warmup
    warmup_steps = math.ceil(len(train_data) * epoch / batch * 0.1)  # 10% of train data for warm-up
    logging.info("Warmup-steps: {}".format(warmup_steps))
    return train_dataloader, train_loss, warmup_steps


def get_evaluator (df, batch, model):

    '''
    prepare data for active learning evaluation
    evaluation is not used but neccessary to run the training
    '''
    print( df.keys())
    logging.info("Read evaluation dataset")
    eval_data = SentencesDataset(examples = DFReader().get_examples(df, max_examples = 10), model = model) # converts to embedding
    eval_dataloader = DataLoader(eval_data, shuffle = False, batch_size = batch)
    evaluator = EmbeddingSimilarityEvaluator(df['text'], df['compare_to_text'], df['y'])

    return eval_dataloader, evaluator



def train_active(df_train, model):
    '''
    define training parameters
    '''

    train_batch_size = 128  # Where does this belong?
    num_epochs = 4  # Where does this belong?
    train_dataloader, loss, warmup_steps = get_train_loader(df_train, train_batch_size, num_epochs, model)
    # eval_dataloader, evaluator = get_evaluator(df_eval, train_batch_size, model)

    '''
    do the training:
    '''

    model.fit(train_objectives=[(train_dataloader, loss)],
              #evaluator=evaluator,
              epochs=num_epochs,
              #evaluation_steps=100,
              warmup_steps=warmup_steps,
              # output_path=model_save_path # will use save below in order to overwrite
              )

    return model
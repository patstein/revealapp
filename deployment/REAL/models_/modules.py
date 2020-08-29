import pandas as pd
import os
import sys
from sentence_transformers import SentencesDataset, LoggingHandler, losses

sys.path.append('/Users/patrickrs/Documents/Github/sentencetransformers/sentencetransformers')
from SentenceTransformer import *  # importing custom version of SentenceTransformer
from deployment.REAL.models_.helpers import update_andor_save_data, get_highlight_sentence, suggest_most_similar_cosine, \
    get_training_pairs, train_active, split_in_sentences


def process_documents(DocumentsRaw, BASE_MODEL_PRETRAINED, path_documents, path_sentences, path_embeddings,
                      path_model_adapted, BlockID=0):
    '''
    This function:
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

    # convert to df:
    df_DocumentsRaw = pd.DataFrame(DocumentsRaw)

    # define paths:
    # BlockID = df_DocumentsRaw.iloc[0]['id_user'] #commented because I found it too risky. You're still only considering the user of the first document                                                    right? What if there are more than one user but the order of the docs changes?
    path_DocumentsRaw = path_documents + str(BlockID) + '.pkl'
    path_Sentences = path_sentences + str(BlockID) + '.pkl'
    path_Embeddings = path_embeddings + str(BlockID) + '.pkl'
    path_model = path_model_adapted + str(BlockID)

    # generate the sentences dataframe from documents:
    df_Sentences = pd.concat(list(
        df_DocumentsRaw.apply(
            split_in_sentences,
            axis=1)))

    # give unique global ID. (Need to rethink how to do it when uploading for second time)
    df_Sentences.reset_index(inplace=True, drop=True)
    df_Sentences['id_sent'] = df_Sentences.index

    # initiate a copy of the pretrained model:
    if not os.path.exists(path_model):
        model = SentenceTransformer(BASE_MODEL_PRETRAINED)
        model.save(path_model)
    else:
        model = SentenceTransformer(path_model)

    # create embeddings:
    corpus = list(df_Sentences['text'])
    df_Embeddings = pd.DataFrame(model.encode(corpus))
    df_Embeddings.index = df_Sentences.index.values
    # df_Embeddings['id_sent'] = df_Embeddings.index

    # save or update data for further training and evaluation:
    update_andor_save_data(df_DocumentsRaw, path_DocumentsRaw)
    update_andor_save_data(df_Sentences, path_Sentences)
    update_andor_save_data(df_Embeddings, path_Embeddings)

    # initiate model for further training and evaluation if there isn't any:
    if not os.path.exists(path_model):
        model.save(path_model)

    # get some stats to return
    doc_records = pd.read_pickle(path_DocumentsRaw).shape[0]
    sent_records = pd.read_pickle(path_Sentences).shape[0]
    embed_records = pd.read_pickle(path_Embeddings).shape[0]

    if sent_records == embed_records:
        message = 'Nr of Docs submitted: {}\nNr of sentences: {}\nNr of embedding vectors created: {}\n'.format(
            doc_records, sent_records, embed_records)

    else:
        message = 'An ERROR occurred here.\nNr of sentences submitted: {}\nNr of embeddings created: {}\nSince the' \
                  'numbers don\'t coincide, investigate here the error!\n'.format(sent_records, embed_records)

    return message


def suggest_similars(Highlights, path_sentences, path_embeddings, path_model_adapted, fuzziness, BlockID=0):
    '''
    This function:
        finds the closest sentences for each UserTag,
        using the pretrained model and the documents uploaded to the block
        saves tags and tags suggestions
    Returns:
        a dataframe of suggested tags whith their suggestion strength, appended to the received highlights
    Arguments:
        UserTags: a table whith tags and parameters of the text belonging them
        BlockID: an ID to identify data and model that belong together
        (default=0; all texts and tags work whith one model)
        fuzziness: 1-fuzziness defines the lower bound for the similarity of the suggestions
    '''

    # convert the input and limit to only the static ones (currently user generated or accepted):
    df_Highlights = pd.DataFrame(Highlights)
    df_Highlights = df_Highlights[(df_Highlights['accepted'] == 1) | (df_Highlights['suggested'] == 0)]

    # define paths:
    # BlockID = df_Highlights.iloc[0]['id_user']
    path_Sentences = path_sentences + str(BlockID) + '.pkl'
    path_Embeddings = path_embeddings + str(BlockID) + '.pkl'
    path_Model = path_model_adapted + str(BlockID)

    # collect the initiated and trained (if already) model:
    model = SentenceTransformer(path_Model)
    # model.eval() # put model into evaluation mode - should not be neccessary

    # collect the previously processed sentences and embeddings:
    df_Sentences = pd.read_pickle(path_Sentences)
    df_Embeddings = pd.read_pickle(path_Embeddings)

    # find the sentences (text and ID of it) corresponding the tags (alternatively, we could use the original):
    if df_Highlights['id_highlight'].isnull()[0]:
        # then the request comes not from the tags table but from the custom search.
        isHighlightSuggestion = False
    else:
        isHighlightSuggestion = True

    if isHighlightSuggestion:
        df_Highlights[['text', 'id_sent']] = df_Highlights.apply(
            get_highlight_sentence,
            args=[df_Sentences],
            axis=1,
            result_type='expand')

    else:
        # Then just take the text
        df_Highlights['id_sent'] = [None] * len(df_Highlights['id_highlight'])

    # flag sentences and their embeddings which are already a Highlight and therefore shouldn't be searched
    # TODO: implement this per tag
    df_Sentences['suggestible'] = ~df_Sentences['id_sent'].isin(df_Highlights['id_sent'])

    # generate tag suggestions for each tag:
    df_Suggestions = pd.concat(list(
        df_Highlights.apply(
            suggest_most_similar_cosine,
            args=[df_Embeddings,
                  df_Sentences,
                  model,
                  1 - fuzziness],  # 1-fuzziness defines the threshold on the similarity score. fuzziness 0 only returns
            # results with similarity 100%.
            axis=1)))

    if isHighlightSuggestion:
        # define IDs for suggested highlights:
        # TODO: ensure no ID conflicts arise on the FS backend side
        df_Suggestions['id_highlight'] = range(
            df_Highlights['id_highlight'].max() + 1,
            df_Highlights['id_highlight'].max() + 1 + len(df_Suggestions))

        # add suggestions:
        # df_Suggestions_all = df_Highlights.append(
        #     df_Suggestions_all).append(
        #     df_Suggestions)
        df_Highlights.drop(['id_sent'], axis=1, inplace=True)
        df_Suggestions.drop(['id_sent_rel', 'suggestible'], axis=1, inplace=True)
        df_Suggestions_all = df_Highlights.append(
            df_Suggestions)
    else:
        df_Suggestions.reset_index(inplace=True, drop=True)
        df_Suggestions['id_highlight'] = df_Suggestions.index
        df_Suggestions.drop(['id_sent_rel', 'suggestible'], axis=1, inplace=True)
        df_Suggestions_all = df_Suggestions

    # df_Suggestions_all.columns = cols_input  # this will be removed after final cleanup

    return df_Suggestions_all  # .to_json(orient = 'records') #?


def retrain(Highlights, path_sentences, path_embeddings, path_model_adapted, BlockID=0):
    '''
    This function:
        actualises (trains) the initialised pretrained model,
        based on user-generated tags and tag evaluations
        finds the closest sentences for each UserTag,
        using the actualised model and the documents uploaded to the block
        saves actualised model, tags and tags suggestions
    Returns:
        a dataframe of suggested tags whith their suggestion sterngth, appended to the received highlights
    Arguments:
        TagSuggestions: a table with previous tag suggestions evaluated by user
        BlockID: an ID to identify data and model that belong together
        (default=0; all texts and tags work whith one model)
    '''
    # convert the input:
    df_Highlights = pd.DataFrame(Highlights)
    # df_Highlights = df_Highlights[(df_Highlights['accepted'] == 1) | (df_Highlights['suggested'] == 0)]

    # define paths:
    # BlockID = df_Highlights.iloc[0]['id_user']
    path_Sentences = path_sentences + str(BlockID) + '.pkl'
    path_Embeddings = path_embeddings + str(BlockID) + '.pkl'
    path_Model = path_model_adapted + str(BlockID)

    # collect the initiated and trained (if already) model:
    model = SentenceTransformer(path_Model)
    # model.eval() # put model into evaluation mode - should not be neccessary

    # collect the previously processed sentences and embeddings:
    df_Sentences = pd.read_pickle(path_Sentences)
    # df_Embeddings = pd.read_pickle(path_Embeddings)

    # find the sentences corresponding the tags (alternatively, we could use the original):
    df_Highlights[['text', 'id_sent']] = df_Highlights.apply(
        get_highlight_sentence,
        args=[df_Sentences],
        axis=1,
        result_type='expand')

    # flag sentences and their embeddings which are already a Highlight and therefore shouldn't be searched
    # TODO: implement this per tag
    df_Sentences['suggestible'] = ~df_Sentences['id_sent'].isin(df_Highlights['id_sent'])

    # create ActiveLearning sentence pairs from suggestion feedback:
    # TODO: don't fail if the function returns an empty dataframe
    df_LearnActive = pd.concat(list(
        df_Highlights.apply(
            get_training_pairs,
            args=[df_Highlights],
            axis=1)))

    # train model on the ActiveLearning sentence pairs:
    model_trained = train_active(df_LearnActive, df_LearnActive, model)

    # create new embeddings for the sentences:
    corpus_sentences = list(df_Sentences['text'])
    df_Embeddings = pd.DataFrame(model.encode(corpus_sentences))
    df_Embeddings.index = df_Sentences.index.values

    # save
    # save the new embeddings:
    update_andor_save_data(df_Embeddings, path_Embeddings, override=True)
    # save the trained model for further training and evaluation:
    model_trained.save(path_Model)

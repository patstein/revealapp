import json
import pandas as pd
#from models.main_model import RevealModel
import os
from time import time
from numba import jit
from line_profiler import LineProfiler

from models.modules import process_documents
from models.modules import retrain
from models.modules import suggest_similars




'''
class RevealModel:
    # load dummy data
    global posted_docs
    posted_docs = json.load(
        open('/Users/patrickrs/Documents/Gitlab/revealapp/50_deployment/REAL/DummyData/DummyDocs.json'))

    def __init__(self, name, debug_mode=False):
        #self.logger, self.config = RevealModel.prepare_environment()
        self.whoami = name

        BASE_MODEL_PRETRAINED = 'bert-base-nli-mean-tokens'

        self.BlockID = ''
        self.fuzziness = 0.2
        self.debug_mode = debug_mode

        if debug_mode:
            path_base = os.path.expanduser("~/Desktop") + '/TEST_revealStorage/'
            self.BASE_MODEL_PRETRAINED = 'PretrainedModels/' + BASE_MODEL_PRETRAINED + '/'
        else:
            path_base = '/home/revealStorage/'
            self.BASE_MODEL_PRETRAINED = '/app/PretrainedModels/' + BASE_MODEL_PRETRAINED + '/'

        self.path_base = path_base

        self.path_model_pretrained = path_base + 'models/pretrained/'  # + BASE_MODEL_PRETRAINED
        self.path_model_adapted = path_base + 'models/adapted/model'  # + str(BlockID)

        self.path_documents = path_base + 'data/raw/documents'  # + str(BlockID)
        self.path_sentences = path_base + 'data/sentences/sentences'  # + str(BlockID)
        self.path_embeddings = path_base + 'data/embeddings/embeddings'  # + str(BlockID)

        self.path_tags = path_base + 'data/tags_user/tags_user'  # + str(BlockID)
        self.path_tags_suggested = path_base + 'data/tags_suggested/tags_suggested'  # + str(BlockID)

        # create folderstructure
        folders_to_be_created = [
            self.path_model_pretrained
            , self.path_model_adapted[:-(self.path_model_adapted[::-1].find('/'))]
            , self.path_documents[:-(self.path_documents[::-1].find('/'))]
            , self.path_sentences[:-(self.path_sentences[::-1].find('/'))]
            , self.path_embeddings[:-(self.path_embeddings[::-1].find('/'))]
            , self.path_tags[:-(self.path_tags[::-1].find('/'))]
            , self.path_tags_suggested[:-(self.path_tags_suggested[::-1].find('/'))]
        ]

        '''  ''' # ACTIVATE for Server
            # create folder structure if not exists:
            global original_umask
            for directory in folders_to_be_created:
                try:
                    if debug_mode and os.path.exists(directory):
                        shutil.rmtree(directory)
                    original_umask = os.umask(0)
                    os.makedirs(directory)
                finally:
                    os.umask(original_umask) 


    #post documents function. Called whenever new docs are uploaded



    def postDocuments(self, posted_docs):
        # takes about 1 min to run

        outputmessage = process_documents(
            DocumentsRaw=posted_docs
            , BASE_MODEL_PRETRAINED=self.BASE_MODEL_PRETRAINED
            , path_documents=self.path_documents
            , path_sentences=self.path_sentences
            , path_embeddings=self.path_embeddings
            , path_model_adapted=self.path_model_adapted
            , BlockID=0
        )

        return outputmessage


    def suggestTags(self, posted_tags):

        # initiate predict engine here:
        suggestedTags_df = suggest_similars(
            Highlights=posted_tags
            , path_sentences=self.path_sentences
            , path_embeddings=self.path_embeddings
            , path_model_adapted=self.path_model_adapted
            , fuzziness=self.fuzziness
            , BlockID=0
        )

        return suggestedTags_df.to_json(orient='records')



    def retrain(self, posted_tags):

        # retrain model
        retrain(
            Highlights=posted_tags
            , path_sentences=self.path_sentences
            , path_embeddings=self.path_embeddings
            , path_model_adapted=self.path_model_adapted
            , BlockID=0
        )



    def setFuzziness(self, posted_fuzziness):
        df_fuzziness = pd.DataFrame(posted_fuzziness)
        val_fuzziness = df_fuzziness['fuzziness'].iloc[0]

        self.fuzziness = val_fuzziness

        return self.fuzziness



    def searchSuggestions(self, search_query):
        df_search_query = pd.DataFrame(search_query)

        # Enriching search query to meet style of usual higlights. Just filled with None s
        dummyColumns = ["id_highlight","id_doc","id_user","id_tag","start_idx","end_idx","category","label","text",
                        "negativetag","suggested","score","id_parent_highlight","accepted","date_created",
                        "date_updated"]
        df_search_query = pd.concat([df_search_query, pd.DataFrame(columns=dummyColumns)])
        df_search_query['suggested'] = 0 # so it's not filtered out

        suggestedTags_df = suggest_similars(
            Highlights=df_search_query
            , path_sentences=self.path_sentences
            , path_embeddings=self.path_embeddings
            , path_model_adapted=self.path_model_adapted
            , fuzziness=self.fuzziness
            , BlockID=0
        )

        return suggestedTags_df.to_json(orient='records')


    # for debugging only
    def getEmbedding(self):
        path_Embeddings = self.path_embeddings + str(0) + '.pkl'
        df_Embeddings = pd.read_pickle(path_Embeddings)

        return df_Embeddings.shape


    def printTest(self):
        folder_to_be_checked = '/app/PretrainedModels/bert-base-nli-mean-tokens.zip'

        if os.path.exists(folder_to_be_checked):
            message = 'exists\n'
        else:
            message = 'does NOT exist\n'

        return message


global reveal_model
reveal_model = RevealModel("RevealApp Model", debug_mode=True)
'''
BASE_MODEL_PRETRAINED = 'bert-base-nli-mean-tokens'
path_base = os.path.expanduser("~/Desktop") + '/TEST_revealStorage/'
path_model_pretrained = path_base + 'models/pretrained/'
path_documents = path_base + 'data/raw/documents'
path_sentences = path_base + 'data/sentences/sentences'  # + str(BlockID)
path_embeddings = path_base + 'data/embeddings/embeddings'  # + str(BlockID)
path_model_adapted = path_base + 'models/adapted/model'
def postDocuments(posted_docs):
    # takes about 1 min to run

    outputmessage = process_documents(
        DocumentsRaw=posted_docs
        , BASE_MODEL_PRETRAINED=BASE_MODEL_PRETRAINED
        , path_documents=path_documents
        , path_sentences=path_sentences
        , path_embeddings=path_embeddings
        , path_model_adapted=path_model_adapted
        , BlockID=0
    )

    return outputmessage
posted = json.load(
        open('/Users/patrickrs/Documents/Gitlab/revealapp/50_deployment/REAL/DummyData/DummyDocs.json'))
lp = LineProfiler()
lp_wrapper = lp(postDocuments)
lp_wrapper(posted)
lp.print_stats()




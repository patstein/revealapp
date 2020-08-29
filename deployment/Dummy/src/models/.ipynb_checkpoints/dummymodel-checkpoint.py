import yaml
import os
import pandas as pd
import requests
import json
import logging
import gzip
from flask import jsonify
from urllib.parse import urlparse

from simple_logging.custom_logging import setup_custom_logger
from json.decoder import JSONDecodeError


class DummyModel:
    def __init__(self, name):
        self.logger, self.config = DummyModel.prepare_environment()
        self.whoami = name

    @staticmethod
    def prepare_environment():
        conf = yaml.safe_load(open("config.yml"))

        # -------------------------------------
        # Set up logger
        # -------------------------------------
        LOGGING_LEVEL = eval(conf['logging_setup']['logging_level'])
        log_file = os.path.join(conf['logging_setup']['log_directory'], 'dummymodel.log')

        log = setup_custom_logger('DUMMY_MODEL_LOGGER', LOGGING_LEVEL, flog=log_file)
        log.newline()

        log.info("Environment prepared")

        return log, conf

    
    
    def postDocuments(self, posted_docs):

        #convert to df:
        posted_docs = pd.DataFrame(posted_docs)
            
#         ##########################################################################
#         ##################### This part is for the REAL version ##################
#         ##########################################################################
#         #initiate embedder here.
#         embedder(posted_docs)
       
        return "Thanks for posting the docs. We are going to take it from here...\n"
       
    
    
    
    
    def suggestTags(self, posted_tags):
        
        #convert to df:
        posted_tags = pd.DataFrame(posted_tags)
        posted_tags = posted_tags[posted_tags['suggested'] == 0]


#         ##########################################################################
#         ##################### This part is for the REAL version ##################
#         ##########################################################################       
#         #initiate predict engine here:
#         suggestedTags_df = predict_engine(posted_tags)



        ##########################################################################
        ################## This part is only for the DUMMY version ###############
        ##########################################################################    
        #the suggestion for each tag is every other tag -> for n tags creating n*n suggestions
        suggestedTags_df = posted_tags.copy()
        suggestedTags_df['id_parent_highlight'] = posted_tags['id_highlight'][0]
        suggestedTags_df['score'] = 0.5
        #suggestedTags_df['accepted'] = None

        for index in posted_tags.index[1:]:
            suggestedTags_next = posted_tags
            suggestedTags_next['id_parent_highlight'] = posted_tags['id_highlight'][index]
            suggestedTags_next['score'] = 0.5
            #suggestedTags_next['Accepted'] = None
            suggestedTags_df = suggestedTags_df.append(suggestedTags_next)

        #suggestedTags_df.reset_index(inplace = True, drop = True)
        new_id = posted_tags['id_highlight'].max() + 1
        suggestedTags_df['id_highlight'] = range(new_id,(suggestedTags_df.shape[0] + new_id))
        suggestedTags_df = posted_tags.append(suggestedTags_df)
        
         
        return suggestedTags_df.to_json(orient='records')
    

    
    
    
    def trainSuggest(self, posted_tags):

        #convert to df:
        posted_tags_all = pd.DataFrame(posted_tags)
        posted_tags = posted_tags_all[posted_tags_all['suggested'] == 0]
        posted_sugg = posted_tags_all[posted_tags_all['suggested'] == 1]

#         ##########################################################################
#         ##################### This part is for the REAL version ##################
#         ##########################################################################       
#         #initiate predict engine here:
#         suggestedTags_df = predict_engine(posted_tags)



        ##########################################################################
        ################## This part is only for the DUMMY version ###############
        ##########################################################################    
        #the suggestion for each tag is every other tag -> for n tags creating n*n suggestions
        suggestedTags_df = posted_tags.copy()
        suggestedTags_df['id_parent_highlight'] = posted_tags['id_highlight'][0]
        suggestedTags_df['score'] = 0.5
        #suggestedTags_df['accepted'] = None

        for index in posted_tags.index[1:]:
            suggestedTags_next = posted_tags
            suggestedTags_next['id_parent_highlight'] = posted_tags['id_highlight'][index]
            suggestedTags_next['score'] = 0.5
            #suggestedTags_next['Accepted'] = None
            suggestedTags_df = suggestedTags_df.append(suggestedTags_next)

        #suggestedTags_df.reset_index(inplace = True, drop = True)
        new_id = posted_tags['id_highlight'].max() + 1
        suggestedTags_df['id_highlight'] = range(new_id,(suggestedTags_df.shape[0] + new_id))
        suggestedTags_df = posted_tags.append(suggestedTags_df)
        
         
        return suggestedTags_df.to_json(orient='records')

    
    
    
#        return posted_tags#.to_json(orient='records')
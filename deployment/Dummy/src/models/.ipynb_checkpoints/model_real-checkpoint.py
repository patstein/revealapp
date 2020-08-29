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
        self.MODEL_PRETRAINED = 'No_model_provided_currently'

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
        posted_docs = pd.DataFrame.from_dict(posted_docs)
            
#         ##########################################################################
#         ##################### This part is for the REAL version ##################
#         ##########################################################################
#         #initiate embedder here.
#         embedder(posted_docs)
        self.MODEL_PRETRAINED = posted_docs['FullText'][0]
       
        return "Thanks for posting the docs. We are going to take it from here...\n"
       
    
    
    def suggestTags(self, posted_tags):
        
        #convert to df:
        posted_tags = pd.DataFrame.from_dict(posted_tags)


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
        suggestedTags_df['TagID'] = posted_tags['ID'][0]
        suggestedTags_df['SimilarityScore'] = 0.5
        suggestedTags_df['Accepted'] = None

        for index in posted_tags.index[1:]:
            suggestedTags_next = posted_tags
            print(index)
            print(posted_tags['ID'].loc[index])
            suggestedTags_next['TagID'] = posted_tags['ID'][index]
            suggestedTags_next['SimilarityScore'] = 0.5
            suggestedTags_next['Accepted'] = None
            suggestedTags_df = suggestedTags_df.append(suggestedTags_next)

        suggestedTags_df.reset_index(inplace = True, drop = True)
        suggestedTags_df['ID'] = suggestedTags_df.index
        
        suggestedTags_df['MODEL_PRETRAINED'] = self.MODEL_PRETRAINED
        
        
        return jsonify(suggestedTags_df.to_dict())
    

    
    def trainSuggest(self, posted_tags, posted_suggTags):

        #convert to df:
        posted_tags = pd.DataFrame.from_dict(posted_tags)
        posted_suggTags = pd.DataFrame.from_dict(posted_suggTags)

        
#         #########################################################################
#         #################### This part is for the REAL version ##################
#         #########################################################################
#         #initiate retrain and predict engine here:
#         retrain_engine(posted_suggTags)    #-> updates model
#         suggestedTags_df = predict_engine(posted_tags)



        
        ##########################################################################
        ################## This part is only for the DUMMY version ###############
        ##########################################################################        
        #the suggestion for each tag is every other tag -> for n tags creating n*n suggestions
        suggestedTags_df = posted_tags.copy()
        suggestedTags_df['TagID'] = posted_tags['ID'][0]
        suggestedTags_df['SimilarityScore'] = 0.5
        suggestedTags_df['Accepted'] = None

        for index in posted_tags.index[1:]:
            suggestedTags_next = posted_tags
            print(index)
            print(posted_tags['ID'].loc[index])
            suggestedTags_next['TagID'] = posted_tags['ID'][index]
            suggestedTags_next['SimilarityScore'] = 0.5
            suggestedTags_next['Accepted'] = None
            suggestedTags_df = suggestedTags_df.append(suggestedTags_next)

        suggestedTags_df.reset_index(inplace = True, drop = True)
        suggestedTags_df['ID'] = suggestedTags_df.index
              
        
        return jsonify(suggestedTags_df.to_dict())
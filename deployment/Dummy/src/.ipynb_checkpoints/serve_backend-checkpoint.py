############################################################
########### FREEZE: No need to change this file ############
############################################################

import gzip
import yaml
import os
import json
import logging
import requests

from urllib.parse import urlparse

from io import BytesIO

from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from flask_script import Manager, Server

from simple_logging.custom_logging import setup_custom_logger
from models.dummymodel import DummyModel

from optparse import OptionParser

# -------------------------------------
# Set up the app
# -------------------------------------
app = Flask(__name__)
# -------------------------------------
# Set up logger
# -------------------------------------

conf = yaml.safe_load(open("config.yml"))
LOGGING_LEVEL = eval(conf['logging_setup']['logging_level'])
log_file = os.path.join(conf['logging_setup']['log_directory'],
                        'web_server.log')

app.logger = setup_custom_logger('FLASK_WEB_SERVER', LOGGING_LEVEL, flog=log_file)
app.logger.newline()
app.logger.info("Flask app started")


# -------------------------------------
# Set up main work-horses
# -------------------------------------
dummy_model = DummyModel("Dummy Model")


@app.route('/healthz', methods=['GET'])
def check_liveliness():
    # Check if the backend is running
    app.logger.info("Got a GET for /healthz")
    ####
    # logic to check health status goes here
    ####
    return Response("Seems alright here.\n", status=200, mimetype='text/plain')


@app.route('/postDocuments', methods=['POST'])
def postDocuments():

    #checking received information (do not change):
    app.logger.info("Got a POST for /postDocuments")

    if len(request.data) == 0:
        app.logger.error("No payload data in request")
        return Response("{'Messsage':'Empty request'}", status=400, mimetype='text/plain')

    global dummy_model

    if dummy_model is None:
        app.logger.error("Model not initialized. This should not happen. Investigate")
        return Response("{'Messsage':'Model not initialized'}", status=400, mimetype='text/plain')

    posted_docs = request.get_json(force = True)

    return_message = dummy_model.postDocuments(posted_docs)

    
    return Response(return_message, status=200, mimetype='text/plain')



@app.route('/suggestTags', methods=['POST'])
def suggestTags():

    #checking received information (do not change):
    app.logger.info("Got a POST for /suggestTags")

    if len(request.data) == 0:
        app.logger.error("No payload data in request")
        return Response("{'Messsage':'Empty request'}", status=400, mimetype='text/plain')

    global dummy_model

    if dummy_model is None:
        app.logger.error("Model not initialized. This should not happen. Investigate")
        return Response("{'Messsage':'Model not initialized'}", status=400, mimetype='text/plain')

    
    
    #receive json:
    posted_tags = request.get_json(force = True)

    Suggested_tags_json = dummy_model.suggestTags(posted_tags)

    
    return Suggested_tags_json




@app.route('/trainSuggest', methods=['POST'])
def trainSuggest():

    app.logger.info("Got a POST for /trainSuggest")

    if len(request.data) == 0:
        app.logger.error("No payload data in request")
        return Response("{'Messsage':'Empty request'}", status=400, mimetype='text/plain')

    global dummy_model

    if dummy_model is None:
        app.logger.error("Model not initialized. This should not happen. Investigate")
        return Response("{'Messsage':'Model not initialized'}", status=400, mimetype='text/plain')


    #receive json:    
    posted_tags = request.get_json(force = True)    
    #the posted json file needs to have two keys "tags" which value is the tag json and "suggTags" which value is the suggested tags json

    Suggested_tags_json = dummy_model.trainSuggest(posted_tags)

    
    return Suggested_tags_json











if __name__ == '__main__':

    manager = Manager(app)

    manager.add_command('runserver', Server(host='0.0.0.0', port=5002))

    manager.run()

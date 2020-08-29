#import yaml
import os
from flask import Flask
from flask import request
from flask import Response

from flask import jsonify
from flask_script import Manager, Server

from models.main_model import RevealModel

app = Flask(__name__)


# -------------------------------------
# Set up main work-horses
# -------------------------------------
reveal_model = RevealModel("RevealApp Model")

@app.route('/')
def hello_world():
    t = 3
    t = 4
    t = 5
    return 'The time is {}, thanks for visiting {}.\nChoose one of the options:\n- check health status: /healthz\n- post docs: /postDocuments\n- let the model suggest tags: /suggestTags\n- retrain the model: /trainSuggest\n'.format(t, __name__)


@app.route('/healthz', methods=['GET'])
def check_liveliness():

    global reveal_model

    # Check if the backend is running
    # app.logger.info("Got a GET for /healthz")
    ####
    # logic to check health status goes here

    ####
    return Response("Seems alright here. {} is running\n".format(reveal_model.whoami), status=200, mimetype='text/plain')


@app.route('/postDocuments', methods=['POST'])
def postDocuments():
    # checking received information (do not change):
    #app.logger.info("Got a POST for /postDocuments")

    if len(request.data) == 0:
        #app.logger.error("No payload data in request")
        return Response("{'Messsage':'Empty request'}", status=400, mimetype='text/plain')

    global reveal_model

    if reveal_model is None:
        #app.logger.error("Model not initialized. This should not happen. Investigate")
        return Response("{'Messsage':'Model not initialized'}", status=400, mimetype='text/plain')

    posted_docs = request.get_json(force=True)

    return_message = reveal_model.postDocuments(posted_docs)

    return Response(return_message, status=200, mimetype='text/plain')


@app.route('/suggestTags', methods=['POST'])
def suggestTags():
    # checking received information (do not change):
    #app.logger.info("Got a POST for /suggestTags")

    if len(request.data) == 0:
        #app.logger.error("No payload data in request")
        return Response("{'Messsage':'Empty request'}", status=400, mimetype='text/plain')

    global reveal_model

    if reveal_model is None:
        #app.logger.error("Model not initialized. This should not happen. Investigate")
        return Response("{'Messsage':'Model not initialized'}", status=400, mimetype='text/plain')

    # receive json:
    posted_tags = request.get_json(force=True)

    Suggested_tags_json = reveal_model.suggestTags(posted_tags)

    return Suggested_tags_json


@app.route('/trainSuggest', methods=['POST'])
def trainSuggest():
    #app.logger.info("Got a POST for /trainSuggest")

    if len(request.data) == 0:
        #app.logger.error("No payload data in request")
        return Response("{'Messsage':'Empty request'}", status=400, mimetype='text/plain')

    global reveal_model

    if reveal_model is None:
        #app.logger.error("Model not initialized. This should not happen. Investigate")
        return Response("{'Messsage':'Model not initialized'}", status=400, mimetype='text/plain')

    # receive json:
    posted_tags = request.get_json(force=True)
    # the posted json file needs to have two keys "tags" which value is the tag json and "suggTags" which value is the suggested tags json

    # executing:
    reveal_model.retrain(posted_tags)
    Suggested_tags_json = reveal_model.suggestTags(posted_tags)

    return Suggested_tags_json



@app.route('/setFuzziness', methods=['POST'])
def setFuzziness():
    #app.logger.info("Got a POST for /trainSuggest")

    if len(request.data) == 0:
        #app.logger.error("No payload data in request")
        return Response("{'Messsage':'Empty request'}", status=400, mimetype='text/plain')

    global reveal_model

    if reveal_model is None:
        #app.logger.error("Model not initialized. This should not happen. Investigate")
        return Response("{'Messsage':'Model not initialized'}", status=400, mimetype='text/plain')

    # receive json:
    posted_fuzziness = request.get_json(force=True)

    # executing:
    fuzziness = reveal_model.setFuzziness(posted_fuzziness)

    return Response("The fuzziness has been set to {}. Going forward suggestions are only returned with similarity "
                    "score of at least {}.\n".format(fuzziness, 1-fuzziness), status=200, mimetype='text/plain')




@app.route('/searchSuggestions', methods=['POST'])
def searchSuggestions():
    if len(request.data) == 0:
        return Response("{'Messsage':'Empty request'}", status=400, mimetype='text/plain')

    global reveal_model

    if reveal_model is None:
        return Response("{'Messsage':'Model not initialized'}", status=400, mimetype='text/plain')

    # receive json:
    search_query = request.get_json(force=True)

    # executing:
    Suggested_tags_json = reveal_model.searchSuggestions(search_query)

    return Suggested_tags_json


# delele this (only for debugging)
@app.route('/trainOnly', methods=['POST'])
def trainOnly():
    #app.logger.info("Got a POST for /trainSuggest")

    if len(request.data) == 0:
        #app.logger.error("No payload data in request")
        return Response("{'Messsage':'Empty request'}", status=400, mimetype='text/plain')

    global reveal_model

    if reveal_model is None:
        #app.logger.error("Model not initialized. This should not happen. Investigate")
        return Response("{'Messsage':'Model not initialized'}", status=400, mimetype='text/plain')

    # receive json:
    posted_tags = request.get_json(force=True)
    # the posted json file needs to have two keys "tags" which value is the tag json and "suggTags" which value is the suggested tags json

    # executing:
    reveal_model.retrain(posted_tags)
    #Suggested_tags_json = reveal_model.suggestTags(posted_tags)

    return 'went through\n'


@app.route('/printEmbeddings', methods=['GET'])
def printEmbedding():
    global reveal_model
    embedding_shape = reveal_model.getEmbedding()
    return str(embedding_shape)

@app.route('/printTest', methods=['GET'])
def printTest():
    global reveal_model
    printTeststr = reveal_model.printTest()
    return str(printTeststr)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

if __name__[0:8] == 'app':
    app.run(host='0.0.0.0')







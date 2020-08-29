import json
import pandas as pd
from deployment.REAL.models_.main_model import RevealModel
import os
from time import time
from numba import jit


# initiate global calls object
global reveal_model
reveal_model = RevealModel("RevealApp Model", debug_mode=True)


actions = {"1": "Load Documents",
           "2": "Suggest Tags",
           "3": "Retrain and Suggest",
           "4": "Retrain Only",
           "5": "Set Fuzziness",
           "6": "Search Suggest",
           "7": "exit"}


while True:
    print("Please enter an action the model should perform:")
    for key, value in actions.items():
        print("{}: {}".format(key, value))

    choice = input("")

    while choice not in actions.keys():
        print("Please enter the number before the action you want to perform:")
        choice = input("")

    # stop if exit
    if actions[choice] == "exit":
        break

    #start working:
    print("The model is performing {} ...\n".format(actions[choice]))



    if actions[choice] == "Load Documents":

        start = time()

        # load dummy data
        with open('DummyData/DummyDocs.json') as json_file:
            posted_docs = json.load(json_file)

        return_message = reveal_model.postDocuments(posted_docs)
        end = time()
        print(return_message)
        print(end-start)


    elif actions[choice] == "Suggest Tags":

        start = time()

        # load dummy data
        with open('DummyData/DummyTags.json') as json_file:
            posted_tags = json.load(json_file)

        Suggested_tags_json = reveal_model.suggestTags(posted_tags)
        #print(type(Suggested_tags_json))
        #print(type(json.dumps(Suggested_tags_json, indent=4)))

        end = time()
        print(json.dumps(Suggested_tags_json, indent=4))
        print(end - start)

    elif actions[choice] == "Retrain and Suggest":
        start = time()
        # load dummy data
        with open('DummyData/DummyTagsFeedback.json') as json_file:
            posted_tags = json.load(json_file)

        reveal_model.retrain(posted_tags)
        # Suggested_tags_json = reveal_model.suggestTags(posted_tags)

        end = time()
        print(json.dumps(Suggested_tags_json, indent=4))
        print(end - start)

    elif actions[choice] == "Retrain Only":
        start = time()
        # load dummy data
        with open('DummyData/DummyTagsFeedback.json') as json_file:
            posted_tags = json.load(json_file)

        reveal_model.retrain(posted_tags)

        end = time()
        print('Model has been updated with the feedback. Thanks!\n')
        print(end - start)


    elif actions[choice] == "Set Fuzziness":
        fuzziness = input('Enter fuzziness as a float between 0 and 1: ')

        posted_fuzziness = pd.DataFrame([float(fuzziness)], columns=["fuzziness"])
        start = time()
        # executing:
        fuzziness = float(reveal_model.setFuzziness(posted_fuzziness))

        end = time()
        print("The fuzziness has been set to {}. Going forward suggestions are only returned with similarity score of "
              "at least {}.\n".format(fuzziness, 1 - fuzziness))
        print(end - start)


    elif actions[choice] == "Search Suggest":

        search_query = input('Enter a search string to find suggestions: ')
        search_query = pd.DataFrame([search_query], columns=["text"])

        start = time()

        # executing:
        Suggested_tags_json = reveal_model.searchSuggestions(search_query)

        end = time()
        print(json.dumps(Suggested_tags_json, indent=4))
        print(end - start)

















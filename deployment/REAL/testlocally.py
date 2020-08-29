import json
import os

#print(os.environ["HOMEPATH"])

#print(os.path.expanduser("~/Desktop"))

# directories = ['/home/sevi/Desktop/TestDirectoryCreated', '/home/sevi/Desktop/TestDirectoryCreated/hello']
#
# for directory in directories:
#     os.umask(0)
#     os.makedirs(directory,exist_ok=True)

with open('DummyData/DummyTags.json') as json_file:
    test_json = json.load(json_file)

print(json.dumps(test_json, indent=4))
print(test_json)
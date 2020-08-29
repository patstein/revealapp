import json

print("DummyDocs:\n")
with open('DummyData/DummyDocs.json') as json_file:
    data = json.load(json_file)
    print(json.dumps(data,indent=4))

print("\n")

print("DummyTags:\n")
with open('DummyData/DummyTags.json') as json_file:
    data = json.load(json_file)
    print(json.dumps(data,indent=4))

print("\n")

print("DummyTagsFeedback:\n")
with open('DummyData/DummyTagsFeedback.json') as json_file:
    data = json.load(json_file)
    print(json.dumps(data,indent=4))

print("\n")

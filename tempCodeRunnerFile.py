import json
with open('userLog.json','r') as outfile:
    data = json.load(outfile)
    print(data)
    print(type(data))
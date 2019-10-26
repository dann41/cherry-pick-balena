import json

message = '{"positions": [{"position": [1, 1], "object": "cherry"}, {"position": [1, 1], "object": "user_1"}]}'

try:
    message_json = json.loads(message)
    print(message_json["positions"])
    for x in message_json["positions"]:
        print(x["position"])
        print(x["object"])
except Exception as inst:
    print("Not a valid payload")
    print(inst)    
import json

message = '{"positions": [{"position": [1, 1], "object": "cherry"}, {"position": [1, 1], "object": "user_1"}]}'

try:
    message_json = json.loads(message)
    print(message_json["positions"])
    for pos in message_json["positions"]:
        point = pos["position"]
        x = point[0]
        y = point[1]
        user = pos["object"]
        print(x)
        print(y)
        print(user)
except Exception as inst:
    print("Not a valid payload")
    print(inst)    
from sense_hat import SenseHat
import paho.mqtt.client as mqtt
import json
import random

MAP_TOPIC = "map"
DIRECTIONS_TOPIC = "directions"

sense = SenseHat()
broker_address = "10.10.169.39"
broker_port = 1883

print("Starting...")

# directions
up = "up"
down = "down"
left = "left"
right = "right"
middle = "middle"

#Set color values
r = (255,0,0) #cherry
g = (0,255,0) #players
b = "blank" #blank

#Basic start map
map = [[b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b]]

def place_cherry():
    map[random.randrange(0, 8)][random.randrange(0, 8)] = "cherry"


def find_user_position(user_id, map):
    for i in range(7):
        for j in range(7):
            if map[i][j] == user_id:
                return i, j
                break
    raise Exception("not found user_id \"{}\"".format(user_id))

def check_wall(x, y):
    new_x = x
    new_y = y
    if y == 8:
        new_y = 7
    elif y == -1:
        new_y = 0
    if x == 8:
        new_x = 7
    elif x == -1:
        new_x = 0
    return new_x, new_y

def check_position_free(x, y):
    if map[x][y] == b:
        return True
    return False

def connect_to_mqtt():
    # Connect to MQTT and setup hooks
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message_received
    client.connect(broker_address, broker_port, 60)
    client.loop_forever()
    return client

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(DIRECTIONS_TOPIC)
    place_cherry() 
    return

def on_message_received(client, userdata, message):
    print("Message received")
    if (message.topic == DIRECTIONS_TOPIC):
        print(message.payload)
        try:
            direction_change = json.loads(message.payload)
            print(direction_change)
            on_direction_change(direction_change["user"], direction_change["direction"])
        except Exception as inst:
            print("Not a valid payload")
            print(inst)
    return

def on_direction_change(user_id, new_direction):
    print("{} - {}".format(user_id, new_direction))
    if direction == middle:
        while True:
            x = randrange(7)
            y = randrange(7)
            if check_position_free(x, y):
                map[x][y] = user_id
                break
    x, y = find_user_position(user_id, map)
    new_x, new_y = transform_direction(x, y, new_direction)
    new_x, new_y = check_wall(new_x, new_y)
    if check_position_free(new_x, new_y):
        map[x][y] = b
        map[new_x][new_y] = user_id
    publish_map(map)
    return

def transform_direction(x, y, direction):
    new_x = x
    new_y = y
    if direction == up:
        new_y += 1
    elif direction == down:
        new_y -=1
    elif direction == right:
        new_x += 1
    elif direction == left:
        new_x -= 1
    elif direction == middle:
        print("middle is pressed")
    else:
        print('bad direction "{}"'.format(direction))
    return new_x, new_y

def map_to_positions(map):
    positions = []
    for row in xrange(1,len(map)):
        for cell in xrange(1,len(map[row])):
            if map[row][cell] == b:
                continue
            current = {
                "object":map[row][cell],
                "position":[row, cell]
            }
            positions.append(current)
    return positions

def publish_map(map):
    positions = {
        "positions":map_to_positions(map)
    }
    client.publish(MAP_TOPIC, json.dumps(positions))
    return

client = connect_to_mqtt()
print("Connected...")

while True:
    sense.show_message("Hello game master!")

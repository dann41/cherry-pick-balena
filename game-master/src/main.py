from sense_hat import SenseHat
import paho.mqtt.client as mqtt
import json
import random

MAP_TOPIC = "map"
DIRECTIONS_TOPIC = "directions"

sense = SenseHat()
broker_address = "10.10.169.39"
broker_port = 1883

# directions
up = "up"
down = "down"
left = "left"
right = "right"

#Set color values
r = (255,0,0) #cherry
g = (0,255,0) #players
b = (0,0,0) #blank

#Basic start map
map = [[b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b],
       [b,b,b,b,b,b,b,b]]

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
    if map[x][y] == g:
        return false
    return true

def connect_to_mqtt():
    # Connect to MQTT and setup hooks
    client = mqtt.Client("P1")
    client.connect(broker_address, broker_port, 60)
    client.subscribe(DIRECTIONS_TOPIC)
    client.on_message = on_message_received
    client.loop_forever()
    return client

def on_message_received(client, userdata, message):
    # Code to parse the message received from MQTT (extract information and call on_direction_change)
    if (message.topic == DIRECTIONS_TOPIC):
        direction_change = json.loads(message)
        on_direction_change(direction_change.user, direction_change.direction)
    return

def on_direction_change(user_id, new_direction):
    print(user_id, new_direction)
    new_x, new_y = transform_direction(x, y, new_direction)
    check_wall(new_x, new_y)
    if check_position_free(new_x, new_y):
        map[new_x, new_y] = g
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
    else:
        print('bad direction "{}"'.format(direction))
    return new_x, new_y

def publish_map(map):
    # Send map to MQTT
    return

client = connect_to_mqtt()

while True:
    sense.show_message("Hello game master!")
    print("MASTER!")

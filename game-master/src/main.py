from sense_hat import SenseHat
import paho.mqtt.client as mqtt
import json

MAP_TOPIC = "map"
DIRECTIONS_TOPIC = "directions"

sense = SenseHat()
broker_address = "10.10.169.39"
broker_port = 1883

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
    # Update map and publish
    print(user_id, new_direction)
    return

def publish_map(map):
    # Send map to MQTT
    return

client = connect_to_mqtt()

while True:
    sense.show_message("Hello game master!")

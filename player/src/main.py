from sense_hat import SenseHat
import paho.mqtt.client as mqtt
from time import sleep
import json
import uuid

# Application state
MAP_TOPIC = "map"
DIRECTIONS_TOPIC = "directions"

sense = SenseHat()
broker_address = "10.10.169.39"
broker_port = 1883

#Set color values
r = (255,0,0) #cherry
g = (0,255,0) #opponent players
b = (0,0,0) #blank
w = (255,255,255) #current player

cherry_color = r
opponent_color = g
current_player = w

def on_message_received(client, userdata, message):
    # Code to parse the message received from MQTT (extract information and call on_map_received)
    print(message.payload)
    board = json.loads(message.payload)
    sense.clear()
    for pos in board["positions"]:
        x = pos["position"][0]
        y = pos["position"][1]
        color = opponent_color
        if pos["object"] == "cherry":
            color = cherry_color
        if pos["object"] == user_id:
            color = current_player
        sense.set_pixel(x, y, color)
    return

def connect_to_mqtt():
    print("Connected")
    # Connect to MQTT and setup hooks
    client = mqtt.Client()
    client.connect(broker_address, broker_port, 60)
    client.subscribe(MAP_TOPIC)
    client.on_message = on_message_received
    client.loop_start()
    return client

def identify_user():
    # Generate UserId
    return uuid.uuid1().hex

def send_direction(client, user_id, new_direction):
    # Send new direction to MQTT
    message = {
        'user': user_id,
        'direction': new_direction
    }
    client.publish(DIRECTIONS_TOPIC, json.dumps(message))
    return

def on_map_received(userId, new_direction):
    # Update map and publish
    return

def display_map(map):
    # Display map
    return

def do_nothing():
    return


cherry = [
    b, b, b, g, g, b, b, b,
    b, b, b, b, g, b, b, b,
    b, b, b, g, b, g, b, b,
    b, b, b, g, b, b, g, b,
    b, b, b, g, b, r, r, b,
    b, r, r, b, r, r, r, r,
    r, r, r, r, b, r, r, b,
    b, r, r, b, b, b, b, b
]


sense.clear()
sense.set_pixels(cherry)
client = connect_to_mqtt()
user_id = identify_user()

while True:
  for event in sense.stick.get_events():
    # Check if the joystick was pressed
    if event.action == "pressed":
        send_direction(client, user_id, event.direction)


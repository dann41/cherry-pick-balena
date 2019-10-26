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

up = "up"
down = "down"
left = "left"
right = "right"

def on_message_received(client, userdata, message):
    # Code to parse the message received from MQTT (extract information and call on_map_received)
    print(message.topic)
    print(message.payload)
    board = json.loads(message.payload)
    print(board)
    sense.clear()
    print(board.keys())
    for pos in board["positions"]:
        x = pos["position"][0]
        y = pos["position"][1]
        sense.set_pixel(x, y, cherry_color)
    return

def connect_to_mqtt():
    print("connect_to_mqtt")
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

client = connect_to_mqtt()
user_id = identify_user()
send_direction(client, user_id, up)

while True:
    while True:
  for event in sense.stick.get_events():
    # Check if the joystick was pressed
    if event.action == "pressed":
      # Check which direction
      if event.direction == "up":
        y -= 1
        if y < 0:
          y = 7
      elif event.direction == "down":
        y += 1
        if y > 7:
          y = 0
      elif event.direction == "left":
        x -= 1
        if x < 0:
          x = 7
      elif event.direction == "right":
        x += 1
        if x > 7:
          x = 0
      elif event.direction == "middle":
        sense.clear()

      #sense.set_pixel(x, y, r)

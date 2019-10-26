from sense_hat import SenseHat
import paho.mqtt.client as mqtt
from time import sleep
import json
import uuid

# Application state
MAP_TOPIC = "map"
DIRECTIONS_TOPIC = "directions"
WINNER_TOPIC = "winner"
KILLED_TOPIC = "killed"

COMPLETED = "completed"
STARTED = "started"

state = STARTED

sense = SenseHat()
broker_address = "192.168.1.47"
broker_port = 1883

#Set color values
r = (255,0,0) #cherry
g = (0,255,0) #opponent players
b = (0,0,0) #blank
w = (255,255,255) #current player

cherry_color = r
opponent_color = g
current_player = w

def on_user_killed(user, position):
    if user_id == user:
        print("I got killed!")
        print_board(lose)
    else:
        print(user + " was killed")

def on_user_won(user, position):
    state = COMPLETED
    if user_id == user:
        print("I win!")
        print_board(win)
    else:
        print("I lose!")
        print_board(lose)

def on_message_received(client, userdata, message):
    # Code to parse the message received from MQTT (extract information and call on_map_received)
    print(message.payload)
    if state == COMPLETED:
        return

    if message.topic == MAP_TOPIC:
        board = json.loads(message.payload)
        display_map(board)
    elif message.topic == KILLED_TOPIC:
        killed = json.loads(message.payload)
        on_user_killed(killed['user'], killed['position'])
    elif message.topic == WINNER_TOPIC:
        killed = json.loads(message.payload)
        on_user_won(killed['user'], killed['position'])
    return

def connect_to_mqtt():
    # Connect to MQTT and setup hooks
    client = mqtt.Client()
    client.connect(broker_address, broker_port, 60)
    client.on_connect = on_connect
    client.on_message = on_message_received
    client.loop_start()
    return client

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MAP_TOPIC)
    client.subscribe(WINNER_TOPIC)
    client.subscribe(KILLED_TOPIC)
    return

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

def display_map(board):
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

def do_nothing():
    print("Sleep")
    sleep(0.5)
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

win = [
    g, g, g, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
    g, g, g, g, g, g, g, g
]

lose = [
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r
]

def print_board(board):
    sense.clear()
    sense.set_pixels(board)

print_board(cherry)
client = connect_to_mqtt()
user_id = identify_user()

def on_event_pressed(event):
    if event.action == "pressed":
        send_direction(client, user_id, event.direction)

sense.stick.direction_up = on_event_pressed
sense.stick.direction_down = on_event_pressed
sense.stick.direction_left = on_event_pressed
sense.stick.direction_right = on_event_pressed
sense.stick.direction_middle = on_event_pressed


while True:
    do_nothing()
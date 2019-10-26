from sense_hat import SenseHat
import json
import uuid 
import paho.mqtt.client as mqtt #import the client1

# Application state

sense = SenseHat()
broker_address = "10.10.169.39:1883"

#Set color values
r = (255,0,0) #cherry
g = (0,255,0) #opponent players
b = (0,0,0) #blank
w = (255,255,255) #current player

up = "up"
down = "down"
left = "left"
right = "right"

def connect_to_mqtt():
    # Connect to MQTT and setup hooks
    client = mqtt.Client("P1") #create new instance
    client.connect(broker_address) #connect to broker
    client.subscribe("map")
    client.on_message = on_message_received
    return client

def identify_user():
    # Generate UserId
    return uuid.uuid1()

def send_direction(client, user_id, new_direction):
    # Send new direction to MQTT
    message = {
        'user': user_id,
        'direction': new_direction
    }
    client.publish("directions", json.dumps(message))
    return

def on_message_received(client, userdata, message):
    # Code to parse the message received from MQTT (extract information and call on_map_received)
    print(message)
    return

def on_map_received(userId, new_direction):
    # Update map and publish
    return

def display_map(map):
    # Display map
    return

client = connect_to_mqtt()
user_id = identify_user()
send_direction(client, user_id, up)

while True:
    sense.show_message("Hello player!")

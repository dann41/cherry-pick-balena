from sense_hat import SenseHat

sense = SenseHat()

#Set color values
r = (255,0,0) #cherry
g = (0,255,0) #opponent players
b = (0,0,0) #blank
w = (255,255,255) #current player


def connect_to_mqtt():
    # Connect to MQTT and setup hooks
    return

def identify_user():
    # Generate UserId
    return

def send_direction(uid, newDirection):
    # Send new direction to MQTT
    return

def on_message_received(message):
    # Code to parse the message received from MQTT (extract information and call on_map_received)
    return

def on_map_received(userId, newDirection):
    # Update map and publish
    return

def display_map(map):
    # Display map
    return


while True:
    sense.show_message("Hello player!")


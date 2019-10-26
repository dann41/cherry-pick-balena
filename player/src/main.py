from sense_hat import SenseHat

sense = SenseHat()

#Set color values
r = (255,0,0) #cherry
g = (0,255,0) #opponent players
b = (0,0,0) #blank
w = (255,255,255) #current player

while True:
    sense.show_message("Hello player!")

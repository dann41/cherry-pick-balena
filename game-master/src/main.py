from sense_hat import SenseHat

sense = SenseHat()

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

while True:
    sense.show_message("Hello game master!")

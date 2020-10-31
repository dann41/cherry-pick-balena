import paho.mqtt.client as mqtt
import json
import random

MAP_TOPIC = "map"
DIRECTIONS_TOPIC = "directions"
WINNER_TOPIC = "winner"
KILLED_TOPIC = "killed"

BROKER_ADDRESS = "192.168.1.47"
BROKER_PORT = 1883

print("Starting...")

# directions
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
MIDDLE = "middle"

CHERRY = "cherry"
BLANK = "blank" #blank

GAME_COMPLETED = "completed"
GAME_STARTED = "started"

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Board:
    def __init__(self, length, game_listener):
        self.length = length
        self.game_listener = game_listener
        self.state = GAME_STARTED
        self.map = [[BLANK for x in range(self.length)] for y in range(self.length)]

    def initialize(self):
        position = self.get_free_position()
        self.map[position.x][position.y] = CHERRY

    def check_position_free(self, position):
        return self.map[position.x][position.y] == BLANK

    def get_free_position(self):
        # TODO fix possible endless loop
        while True:
            position = get_random_position(self.length)
            if self.check_position_free(position):
                return position
        return Position(0, 0)
        
    def get_player(self, user_id, create_if_needed):
        for i in range(self.length):
            for j in range(self.length):
                if self.map[i][j] == user_id:
                    return Player(user_id, Position(i, j))

        if create_if_needed:
            return Player(user_id, self.get_free_position())
        else:
            raise Exception("not found user_id \"{}\"".format(user_id))   

    def update_player(self, user_id, direction):
        if self.state == GAME_COMPLETED:
            print("Game completed. Do nothing")
            return

        user = self.get_player(user_id, direction == MIDDLE)
        new_position = self.transform_direction(user.position, direction)

        if self.map[new_position.x][new_position.y] == CHERRY:
            print("Game completed. Winner: " + user_id)
            self.state = GAME_COMPLETED
            self.game_listener.on_game_completed(Player(user_id, new_position))
        elif self.map[new_position.x][new_position.y] != BLANK:
            player_killed = Player(self.map[new_position.x][new_position.y], new_position)
            self.game_listener.on_player_killed(player_killed)

        self.map[user.position.x][user.position.y] = BLANK
        self.map[new_position.x][new_position.y] = user.user_id
        self.game_listener.on_board_updated(self.map, self.length)

    def transform_direction(self, position, direction):
        if direction == UP:
            return Position(position.x, (self.length + position.y - 1) % self.length)
        elif direction == DOWN:
            return Position(position.x, (self.length + position.y + 1)  % self.length)
        elif direction == RIGHT:
            return Position((self.length + position.x + 1) % self.length, position.y)
        elif direction == LEFT:
            return Position((self.length + position.x - 1) % self.length, position.y)
        elif direction == MIDDLE:
            return self.get_free_position()
        else:
            print('bad direction "{}"'.format(direction))
            return Position(0, 0)

class Player:
    def __init__(self, user_id, position):
        self.user_id = user_id
        self.position = position

class GameListener:
    def __init__(self, client):
        self.client = client

    def on_board_updated(self, map, length):
        positions = {
            "positions": serialize_map(map, length)
        }
        self.client.publish(MAP_TOPIC, json.dumps(positions))

    def on_player_killed(self, player):
        player_json = {
            "user": player.user_id,
            "position": {
                "x": player.position.x,
                "y": player.position.y,
            }
        }
        self.client.publish(KILLED_TOPIC, json.dumps(player_json))

    def on_game_completed(self, winner):
        player_json = {
            "user": winner.user_id,
            "position": {
                "x": winner.position.x,
                "y": winner.position.y,
            }
        }
        self.client.publish(WINNER_TOPIC, json.dumps(player_json))        


def get_random_position(length):
    return Position(random.randrange(0, length), random.randrange(0, length))

def connect_to_mqtt(mqtt_client):
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message_received
    mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    mqtt_client.loop_forever()
    return mqtt_client

def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_client.subscribe(DIRECTIONS_TOPIC)
    return

def on_message_received(mqtt_client, userdata, message):
    if (message.topic == DIRECTIONS_TOPIC):
        try:
            direction_change = json.loads(message.payload)
            on_direction_change(mqtt_client, direction_change["user"], direction_change["direction"])
        except Exception as inst:
            print("Not a valid payload")
            print(inst)
    return

def serialize_map(map, length):
    positions = []
    for row in range(length):
        for cell in range(length):
            if map[row][cell] == BLANK:
                continue
            current = {
                "object":map[row][cell],
                "position":[row, cell]
            }
            positions.append(current)
    return positions

def on_direction_change(mqtt_client, user_id, new_direction):
    print("{} - {}".format(user_id, new_direction))
    board.update_player(user_id, new_direction)

# Init
client = mqtt.Client()
board = Board(8, GameListener(client))

# Start
board.initialize()
connect_to_mqtt(client)

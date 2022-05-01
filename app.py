from flask import Flask, render_template, request
from flask_socketio import SocketIO
from numpy import broadcast
from game_backend import Game
from time import sleep

app = Flask(__name__)
socketio = SocketIO(app)
game = Game(hidden_monsters=False)

@app.route("/")
def index():
    map = game.getMap()
    return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]) )

@socketio.on("join")
def on_join_msg(json):
    player_id = json["id"]
    print(f"received new join message from {player_id}")
    if not(player_id in game.getPlayers().keys()):
        data = game.addPlayer(player_id)
        socketio.emit("you_joined", {"lifes": game.getPlayers()[player_id].getLife()}, to=player_id)
        socketio.emit("new_user", {"data": data})
    else:
        socketio.emit("you have already joined", to=player_id)

@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    player_id = json["id"]
    print(f"received move ws message from {player_id}")
    dx = json['dx']
    dy = json["dy"]
    data, ret, win_a_life = game.move(dx, dy, player_id)
    if ret:
        socketio.emit("response", {"data": data, "win_a_life": win_a_life, "id": player_id} )

@socketio.on("is_hit?")
def on_is_hit_msg(json):
    player_id = json["id"]
    print(f"received is_hit? ws message from {player_id}")
    is_near, is_hit, n_hits, is_dead, monsters_locations, data = game.is_hit(player_id)
    if is_near:
        socketio.emit("hit_by_monsters", {"n_hits": n_hits,"is_hit": is_hit, "monsters_locations": monsters_locations}, to=player_id)
        if is_dead:
            print(f"GAME OVER for the player {player_id}")
            socketio.emit("game_over", to=player_id)
            game.removePlayer(player_id)
            socketio.emit("a player died", data)



@socketio.on("shoot")
def on_shoot_msg(json):
    player_id = json["id"]
    print(f"received shoot message from {player_id} ")
    hit, hit_player, is_dead, data = game.hitOpponent(player_id)
    if hit:
        socketio.emit("shoot result", "you got it", to=player_id)
        socketio.emit("you_got_shot",  to=hit_player)
        if is_dead:
            print(f"GAME OVER for the player {hit_player}")
            socketio.emit("game_over", to=hit_player)
            socketio.emit("a player died", data)
    else:
        socketio.emit("shoot result", "you missed", to=player_id)

if __name__=="__main__":
    socketio.run(app, port=5001)



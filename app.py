from flask import Flask, render_template, request
from flask_socketio import SocketIO
from numpy import broadcast
from game_backend import Game

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()

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
    print("received move ws message")
    dx = json['dx']
    dy = json["dy"]
    player_id = json["id"]

    data, ret, win_a_life = game.move(dx, dy, player_id)
    if ret:
        socketio.emit("response", {"data": data, "win_a_life": win_a_life, "id": player_id} )

@socketio.on("is_hit?")
def on_is_hit_msg(json):
    print("received is_hit? ws message")
    player_id = json["id"]
    is_hit, n_hits, is_dead, monsters_locations = game.hits(player_id)
    print(is_hit, n_hits)
    if is_hit:
        socketio.emit("hit_by_monsters", {"n_hits": n_hits, "monsters_locations": monsters_locations}, to=player_id)
        if is_dead:
            print("GAME OVER for the player")
            socketio.emit("game_over", to=player_id)
    
    

if __name__=="__main__":
    socketio.run(app, port=5001)



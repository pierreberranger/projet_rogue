from flask import Flask, make_response, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
from numpy import broadcast
from game_backend import game
from game_backend.game_index import *

app = Flask(__name__)
socketio = SocketIO(app)
game_index = GameIndex()
player_index = dict()
game = Game(hidden_monsters=True)

@app.route("/play")
def play():
    game_id = request.args.get("game_id", default=None)
    multi = request.args.get("multi") == "1"
    if game_id==None and (request.cookies.get('game_id')==None or multi):
        game_id = generateId(game_index)
        game = Game(multiplayer=multi)
        game_index[game_id] = game
    elif not(multi): 
        game_id = request.cookies.get('game_id')
    if not (game_id in game_index.keys()):
        return render_template("unexisting_id.html")
    
    game = game_index[game_id]
    
    if game.isMultiplayer() != multi:
        return render_template("unexisting_id.html")
    map = game.getMap()
    nb_players = len(game.getPlayers())
    if nb_players>1 and not(game.isMultiplayer()):
        return render_template("to_many_players.html")
    return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]), game_id=game_id, multi=multi)

@app.route("/")
def welcome():
    return render_template("welcome.html")


@socketio.on("join")
def on_join_msg(json):
    room = json["room"]
    socket_id = json["id"]
    player_id = json["player_id"]
    game = game_index[room]
    player_index[player_id] = socket_id
    print(f"received new join message from {socket_id}")
    join_room(room)
    if not(player_id in game.getPlayers().keys()):
        data = game.addPlayer(player_id)
        socketio.emit("you_joined", {"lifes": game.getPlayers()[player_id].getLife()}, to=player_index[player_id])
        socketio.emit("new_user", {"data": data}, room=room)
    else:
        socketio.emit("you have already joined", to=player_index[player_id])


@socketio.on("get a saved game")
def save_msg(json):
    socket_id = json["id"]
    player_id = json["player_id"]
    room = json["room"]
    join_room(room)
    game = game_index[room]
    try:
        check_id(player_id, socket_id)
    except KeyError :
        player_index[player_id] = socket_id
    if len(game.getPlayers())==0:
        data = game.addPlayer(player_id)
        socketio.emit("new_user", {"data": data}, room=room)
        player_index[player_id] = socket_id
    socketio.emit("you_joined", {"lifes": game.getPlayers()[player_id].getLife()}, to=player_index[player_id])

@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    room = json["room"]
    socket_id = json["id"]
    player_id = json["player_id"]
    check_id(player_id, socket_id)
    game = game_index[room]
    print(f"received move ws message from {player_id}")
    dx = json['dx']
    dy = json["dy"]
    data, ret, win_a_life = game.move(dx, dy, player_id)
    if ret:
        socketio.emit("response", {"data": data, "win_a_life": win_a_life, "id": player_id}, room=room )

@socketio.on("is_hit?")
def on_is_hit_msg(json):
    room = json["room"]
    socket_id = json["id"]
    player_id = json["player_id"]
    check_id(player_id, socket_id)
    game = game_index[room]
    print(f"received is_hit? ws message from {player_id}")
    is_near, is_hit, n_hits, is_dead, monsters_locations, data = game.is_hit(player_id)
    if is_near:
        socketio.emit("hit_by_monsters", {"n_hits": n_hits,"is_hit": is_hit, "monsters_locations": monsters_locations}, to=player_index[player_id])
        if is_dead:
            print(f"GAME OVER for the player {player_id}")
            socketio.emit("game_over", to=player_index[player_id])
            game.removePlayer(player_id)
            socketio.emit("a player died", data, room=room)



@socketio.on("shoot")
def on_shoot_msg(json):
    room = json["room"]
    socket_id = json["id"]
    player_id = json["player_id"]
    check_id(player_id, socket_id)
    game = game_index[room]
    print(f"received shoot message from {player_id} ")
    hit, hit_player, is_dead, data = game.hitOpponent(player_id)
    if hit:
        socketio.emit("shoot result", "you got it", to=player_index[player_id])
        socketio.emit("you_got_shot",  to=hit_player)
        if is_dead:
            print(f"GAME OVER for the player {hit_player}")
            socketio.emit("game_over", to=hit_player)
            socketio.emit("a player died", data)
            game.removePlayer(hit_player)
    else:
        socketio.emit("shoot result", "you missed", to=player_index[player_id])

@socketio.on("disconnected")
def on_disconnect_msg(json):
    room = json["room"]
    player_id = json["player_id"]
    print(f"received disconnect message from {player_id} ")
    leave_room(room)

def check_id(player_id, socket_id):
    if not(player_id in player_index):
        raise KeyError
    if player_index[player_id] != socket_id:
        player_index[player_id] = socket_id


if __name__=="__main__":
    socketio.run(app, port=5001)



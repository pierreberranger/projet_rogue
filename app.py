from flask import Flask, render_template 
from flask_socketio import SocketIO
from game_backend import Game

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()


@app.route("/")
def index():
    map = game.getMap()
    return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]), n_life=game.getLife() )

@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    print("received move ws message")
    dx = json['dx']
    dy = json["dy"]

    data, ret, win_a_life = game.move(dx,dy)
    if ret:
        socketio.emit("response", {"data": data, "win_a_life": win_a_life} )

@socketio.on("is_hit?")
def on_is_hit_msg():
    print("received is_hit? ws message")
    is_hit, n_hits, is_dead, monsters_locations = game.hits()
    print(is_hit, n_hits)
    if is_hit:
        socketio.emit("hit", {"n_hits": n_hits, "monsters_locations": monsters_locations})
        if is_dead:
            print("GAME OVER for the player")
            socketio.emit("game_over")
    
    

if __name__=="__main__":
    socketio.run(app, port=5001)



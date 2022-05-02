


window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );
    var message = document.getElementById("message");
    message.innerHTML = `press enter to join the game`;
    var room = document.getElementById("game_id").innerText;


    document.onkeydown = function(e){
        switch(e.keyCode){
            case 37:
                socket.emit("move", {dx:-1, dy:0, id: socket.id, room:room});
                break;
            case 38:
                socket.emit("move", {dx:0, dy:-1, id: socket.id, room:room});
                break;
            case 39:
                socket.emit("move", {dx:1, dy:0, id: socket.id, room:room});
                break;
            case 40:
                socket.emit("move", {dx:0, dy:1, id: socket.id, room:room});
                break;
            case 13:
                socket.emit("join", {id: socket.id, room:room});
                break;
            case 32:
                socket.emit("shoot", {id: socket.id, room:room});
                console.log("shoot");
                break;
        }


    };
    
    var btn_n = document.getElementById("go_n");
    btn_n.onclick = function(e) {
        console.log("Clicked on button north");
        socket.emit("move", {dx:0, dy:-1, id:socket.id, room:room});
    };

    var btn_s = document.getElementById("go_s");
    btn_s.onclick = function(e) {
        console.log("Clicked on button south");
        socket.emit("move", {dx:0, dy:1, id:socket.id, room:room});
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        console.log("Clicked on button w");
        socket.emit("move", {dx:-1, dy:0, id:socket.id, room:room});
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        console.log("Clicked on button e");
        socket.emit("move", {dx:1, dy:0, id:socket.id, room:room});
    };

    socket.on("you_joined", function(data){
        message.innerHTML = "you joined successfully!";
        for(var i=0; i<data.lifes; i++){
            var lifes = document.getElementById("life_bar");
            life_to_add = document.createElement("span");
            life_to_add.classList.add("life");
            life_to_add.innerHTML = `<img src="static\\life.png" alt=""></img>`;
            lifes.appendChild(life_to_add);
        }
    })
    socket.on("you have already joined", function(){
        message.innerHTML = "you have already joined"
    })
    socket.on("new_user", function(received_data){
        data = received_data.data;
        var cell_id = "cell " + data.i + "-" + data.j;
        var span_to_modif = document.getElementById(cell_id);
        span_to_modif.innerHTML = data.content;

    })
    socket.on("response", function(received_data){
        data = received_data.data;
        win_a_life = received_data.win_a_life;
        player_id = received_data.id;
        for( var i=0; i<2; i++){
            var cell_id = "cell " + data[i].i + "-" + data[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.innerHTML = data[i].content;
        }
        if (win_a_life && (socket.id == player_id)){
            var lifes = document.getElementById("life_bar");
            life_to_add = document.createElement("span");
            life_to_add.classList.add("life") ;
            life_to_add.innerHTML = `<img src="static\\life.png" alt=""></img>`;
            lifes.appendChild(life_to_add);
            message.innerHTML = "congratuations you got an extra life !";
            clean(500);
        }
        socket.emit("is_hit?", {id: socket.id, room:room});
    });

    socket.on("hit_by_monsters", async function(data){
        console.log(data);
        n_hits = data.n_hits;
        monsters_locations = data.monsters_locations;
        message.innerHTML = `${n_hits} monsters hit you`
        clean(500);
        var lifes = document.getElementById("life_bar");
        console.log(lifes.children);
        for (var i=0; i<n_hits; i++){
            if (lifes.children.length > 1){
                lifes.removeChild(lifes.lastChild);
            }
        }
        for( var i=0; i<monsters_locations.length; i++){
            var cell_id = "cell " + monsters_locations[i].i + "-" + monsters_locations[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.innerHTML = monsters_locations[i].content;
        }
        await new Promise(resolve => setTimeout(resolve, 500));
        console.log({id: socket.id});
        socket.emit("is_hit?", {id: socket.id, room:room});
    });

    socket.on("shoot result", function(response){
        console.log(response);
        message.innerHTML = response;
        clean(500);
    } )
    socket.on("you_got_shot", function(){
        console.log("you_got_shot");
        message.innerHTML = "you_got_shot";
        clean(500);
        var lifes = document.getElementById("life_bar");
        console.log(lifes.children);
        if (lifes.children.length > 1){
            lifes.removeChild(lifes.lastChild);
        }
    } )
    socket.on("a player died", function(data){
        console.log("a new player died");
        message.innerHTML = "a new player died";
        clean(500);
        var cell_id = "cell " + data.i + "-" + data.j;
        var span_to_modif = document.getElementById(cell_id);
        span_to_modif.innerHTML = data.content;

    } )
    socket.on("game_over", function(){
        console.log("game_over");
        socket.emit("disconnect", {id: socket.id, room:room})
        socket.disconnect();
        message.innerHTML = "GAME OVER"
    } )

    async function clean(ms){
        await new Promise(resolve => setTimeout(resolve, ms));
        message.innerHTML = "";

    }

});


window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );

    document.onkeydown = function(e){
        switch(e.keyCode){
            case 37:
                socket.emit("move", {dx:-1, dy:0});
                break;
            case 38:
                socket.emit("move", {dx:0, dy:-1});
                break;
            case 39:
                socket.emit("move", {dx:1, dy:0});
                break;
            case 40:
                socket.emit("move", {dx:0, dy:1});
                break;
        }


    };
    
    var btn_n = document.getElementById("go_n");
    btn_n.onclick = function(e) {
        console.log("Clicked on button north");
        socket.emit("move", {dx:0, dy:-1});
    };

    var btn_s = document.getElementById("go_s");
    btn_s.onclick = function(e) {
        console.log("Clicked on button south");
        socket.emit("move", {dx:0, dy:1});
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        console.log("Clicked on button w");
        socket.emit("move", {dx:-1, dy:0});
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        console.log("Clicked on button e");
        socket.emit("move", {dx:1, dy:0});
    };


    socket.on("response", function(received_data){
        console.log(received_data);
        data = received_data.data;
        win_a_life = received_data.win_a_life
        var message = document.getElementById("message");
        message.innerHTML = "";
        for( var i=0; i<2; i++){
            var cell_id = "cell " + data[i].i + "-" + data[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = data[i].content;
        }
        if (win_a_life){
            var lifes = document.getElementById("life");
            life_to_add = document.createElement("span");
            life_to_add.innerHTML = "£";
            lifes.appendChild(life_to_add);
            message.innerHTML = "congratuations you got an extra life !";
        }
        socket.emit("is_hit?");
    });

    socket.on("hit", async function(data){
        console.log(data);
        n_hits = data.n_hits;
        monsters_locations = data.monsters_locations;
        var message = document.getElementById("message");
        message.innerHTML = `${n_hits} opponents hit you`
        var lifes = document.getElementById("life");
        console.log(lifes.children);
        for (var i=0; i<n_hits; i++){
            if (lifes.children.length > 1){
                lifes.removeChild(lifes.lastChild);
            }
        }
        for( var i=0; i<monsters_locations.length; i++){
            var cell_id = "cell " + monsters_locations[i].i + "-" + monsters_locations[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = monsters_locations[i].content;
        }
        await new Promise(resolve => setTimeout(resolve, 1000));
        socket.emit("is_hit?");
    });

    socket.on("game_over", function(){
        console.log("game_over")
    } )



});
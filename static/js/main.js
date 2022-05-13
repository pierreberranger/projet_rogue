


window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );
    var message = document.getElementById("message");
    message.innerHTML = `press enter to join the game`;
    var room = document.getElementById("game_id").innerText;
    var player_id = getCookie("player_id");
    var multi = true;
    var joined = false;
    
    
    /* we test if we have a multiplayer game or not, the following buttons are implemented only for singleplayer mode*/
    var save_game_button = document.getElementById("save_game")
    if (save_game_button !=null){
        multi = false;
        save_game_button.onclick = function() {
            console.log("pressed save game button");
            setCookie("game_id", `${room}`);
        }
    }
    var new_level_button = document.getElementById("new_level")
    if (new_level_button !=null){
        new_level_button.onclick = function() {
            console.log("pressed new level button");
            document.cookie = 'game_id=; Max-Age=-99999999;'
            socket.emit("disconnected", {id: socket.id, room:room, player_id:player_id})
            socket.disconnect();
        }
    }


    /* some usefull functions*/

    /*clean the message box after a few times*/
    async function clean(ms, message){
        await new Promise(resolve => setTimeout(resolve, ms));
        if (message.innerHTML != "GAME OVER"){
            message.innerHTML = "";
            console.log(message);
        }

    }

    function getCookie(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }
        return null;
    }

    function setCookie(name,value,days) {
        console.log(`changed ${name} cookie`)
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + ";expires=Sat," + expires ;
    }
    /*movement, shoot and join button*/
    document.onkeydown = function(e){

        switch(e.keyCode){
            case 37:
                if (joined){
                    socket.emit("move", {dx:-1, dy:0, id: socket.id, room:room, player_id:player_id});
                }
                    break;
            case 38:
                if (joined){
                    socket.emit("move", {dx:0, dy:-1, id: socket.id, room:room, player_id:player_id});
                }
                break;
            case 39:
                if (joined){
                    socket.emit("move", {dx:1, dy:0, id: socket.id, room:room, player_id:player_id});
                }
                    break;
            case 40:
                if (joined){
                    socket.emit("move", {dx:0, dy:1, id: socket.id, room:room, player_id:player_id});
                }
                    break;
            case 13:
                if (player_id == null){
                    console.log("pressed enter: join");
                    setCookie("player_id", socket.id, 7);
                    player_id = getCookie("player_id");
                    socket.emit("join", {id: socket.id, room:room, player_id:player_id});
                }
                else if(multi){
                    console.log("pressed enter: join");
                    socket.emit("join", {id: socket.id, room:room, player_id:player_id});
                }
                else{
                    console.log("pressed enter: get a saved game");
                    socket.emit("get a saved game", {id: socket.id, room:room, player_id:player_id});
                }
                break;
            case 32:
                if (joined){
                    socket.emit("shoot", {id: socket.id, room:room, player_id:player_id});
                }
                    console.log("pressed space bar: shoot");
                break;
            
        }
        


    };
    
    var btn_n = document.getElementById("go_n");
    btn_n.onclick = function(e) {
        console.log("Clicked on button north");
        if (joined){
            socket.emit("move", {dx:0, dy:-1, id: socket.id, room:room, player_id:player_id});
        }
    };

    var btn_s = document.getElementById("go_s");
    btn_s.onclick = function(e) {
        console.log("Clicked on button south");
        if (joined){
            socket.emit("move", {dx:0, dy:1, id: socket.id, room:room, player_id:player_id});
        }
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        console.log("Clicked on button w");
        if (joined){
            socket.emit("move", {dx:-1, dy:0, id: socket.id, room:room, player_id:player_id});
        }
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        console.log("Clicked on button e");
        if (joined){
            socket.emit("move", {dx:1, dy:0, id: socket.id, room:room, player_id:player_id});
        }
    };


    /*response to server messages*/
    socket.on("you_joined", function(data){
        console.log("you joined");
        joined = true;
        message.innerText = "you joined successfully! \n use the buttons or the keyboard arrows to move, space bar to shoot your ennemies ";
        var lifes = document.getElementById("life_bar");
        lifes.innerHTML="<span>Lives : </span>";
        for(var i=0; i<data.lifes; i++){
            life_to_add = document.createElement("span");
            life_to_add.classList.add("life");
            life_to_add.innerHTML = `<img src="static\\life.png" alt=""></img>`;
            lifes.appendChild(life_to_add);
        }
    })

    socket.on("you have already joined", function(){
        console.log("you have already joined");
        message.innerHTML = "you have already joined"
    })

    socket.on("new_user", function(received_data){
        console.log("new user");
        var data = received_data.data;
        var cell_id = "cell " + data.i + "-" + data.j;
        var span_to_modif = document.getElementById(cell_id);
        span_to_modif.innerHTML = data.content;

    })
    socket.on("change level", function(map){
        console.log("received new map");
        var console_object = document.getElementById("console");
        for(var i=0; i<map.length; i++){
            for (var j=0; j<map[0].length; j++){
                if (map[i][j] == "#") {
                    console_object.children[i].children[j].innerHTML = "";
                    console_object.children[i].children[j].classList = ["mapcell"];
                    console_object.children[i].children[j].classList.add("bloc");
                }
                                
                else if (map[i][j] == "£" ){
                    console_object.children[i].children[j].innerHTML = `<img src="static\\life.png" sizes=""></img>`;
                    console_object.children[i].children[j].classList = ["mapcell"] ;
                    console_object.children[i].children[j].classList.add("accessiblemapcell");
                }
                else if (map[i][j] == "@" ){
                    console_object.children[i].children[j].innerHTML = `<img src="static\\player.png" sizes=""></img>`;
                    console_object.children[i].children[j].classList = ["mapcell"];
                    console_object.children[i].children[j].classList.add("accessiblemapcell");
                    
                }
                else if (map[i][j] == "§" ){
                    console_object.children[i].children[j].innerHTML = `<img src="static\\monster4.png" sizes=""></img>`;
                    console_object.children[i].children[j].classList = ["mapcell"];
                    console_object.children[i].children[j].classList.add("accessiblemapcell");
                   
                }
                else if (map[i][j] == "_" || map[i][j] == "^" ){
                    console_object.children[i].children[j].innerHTML = `<img src="static\\ladder.png" sizes=""></img>`;
                    console_object.children[i].children[j].classList = ["mapcell"];
                    console_object.children[i].children[j].classList.add("accessiblemapcell");
                    
                }
                else if (map[i][j] == "%") {
                    console.log("coucou")
                    console_object.children[i].children[j].innerHTML = `<img src="static\\vaccin.png" sizes=""></img>`;
                    console_object.children[i].children[j].classList = ["mapcell"];
                    console_object.children[i].children[j].classList.add("accessiblemapcell");
                    
                }
                else{
                    console_object.children[i].children[j].innerHTML = ``;
                    console_object.children[i].children[j].classList = ["mapcell"];
                    console_object.children[i].children[j].classList.add("accessiblemapcell");
                }
                
                
                        
            }
        }
    })

    socket.on("moove response", function(received_data){
        console.log("received moove response");
        var data = received_data.data;
        var win_a_life = received_data.win_a_life;
        var id = received_data.id;
        var new_weapon = received_data.new_weapon;
        for( var i=0; i<2; i++){
            var cell_id = "cell " + data[i].i + "-" + data[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.innerHTML = data[i].content;
        }
        if (win_a_life && (id == player_id)){
            var lifes = document.getElementById("life_bar");
            life_to_add = document.createElement("span");
            life_to_add.classList.add("life") ;
            life_to_add.innerHTML = `<img src="static\\life.png" alt=""></img>`;
            lifes.appendChild(life_to_add);
            message.innerHTML = "congratuations you got an extra life !";
            clean(1000, "clean life message");
        }
        if (new_weapon && (id == player_id)){
            message.innerHTML = "congratulations you found a new weapon, your accuracy increased!";
            clean(1000, "clean new weapon message");
        }
        /*because of monsters, after each movement we have to check if the player is not 
        near one (or several) monster and in that case if the monsters hit the player*/
        socket.emit("is_hit?", {id: socket.id, room:room, player_id:player_id});
    });

    /* here is the response to the is_hit message sent to the server, and means that the player has been hit,
     we therefore have to ask if the player is_hit again, in case the player stays near a monster. */
    socket.on("hit_by_monsters", async function(data){
        console.log("hit by monsters");
        var n_hits = data.n_hits;
        var monsters_locations = data.monsters_locations;
        if (n_hits == 0){
            message.innerHTML = "a monster tried to hit you";
            clean(1000, "clean try to hit you message");

        }
        else{
            message.innerHTML = `${n_hits} monsters hit you`;  
            clean(1000, "clean hit by monster message");
        }
        
        var lifes = document.getElementById("life_bar");
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
        await new Promise(resolve => setTimeout(resolve, 500));/*we wait a bit before sending again a is_hit message,
        in order to let the player shoot back or move (if he is quick enough)*/ 
        socket.emit("is_hit?", {id: socket.id, room:room, player_id:player_id});
    });

    socket.on("shoot result", function(response){
        console.log(response);
        message.innerHTML = response;
        clean(1000, "clean shoot result message");
    } )

    socket.on("you_got_shot", function(){
        console.log("you_got_shot");
        message.innerHTML = "you_got_shot";
        clean(1000, "clean got shot message");
        var lifes = document.getElementById("life_bar");
        if (lifes.children.length > 1){
            lifes.removeChild(lifes.lastChild);
        }
    } )
    socket.on("a player died", function(data){
        console.log("a new player died");
        message.innerHTML = "a new player died";
        clean(1000, "clean died message");
        var cell_id = "cell " + data.i + "-" + data.j;
        var span_to_modif = document.getElementById(cell_id);
        span_to_modif.innerHTML = data.content;

    } )
    socket.on("game_over", function(){
        console.log("game_over");
        socket.emit("disconnected", {id: socket.id, room:room, player_id:player_id})
        socket.disconnect();
        message.innerHTML = "GAME OVER";
    } ) 
});
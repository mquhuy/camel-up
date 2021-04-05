<template>
  <div id="registration" v-if="!registered">
    <div class="human-player">
      <input type="checkbox" v-model="addHuman"> Include Human Player
      <input v-if="addHuman" v-model="pName" placeholder="Enter your name">
    </div>
    <input v-model.number="nP" type="number" placeholder="Number of bot players">
    <button v-on:click="register(pName, nP)">Register</button>
  </div>
  <div class="buttons">
      <button v-on:click="start">Start Game</button>
      <button v-on:click="next_player">End turn</button>
  </div>
  <div class="container">
    <div v-if="this.spaces" class="game-board">
      <Space v-for="i in 16" :key="this.spaces[i]" :info=this.spaces[i] />
      <div class="pyramid">
        <Pyramid :action_info="this.actions" :key="this.actions" />
      </div>
    </div>
    <div class="grade-board">
      <div id="players" v-for="player in this.players" :key="player.id">
      <Player :playerName=player.name :playerId=player.id :currentP=this.currentP :points=player.points />
      </div>
    </div>
  </div>
</template>

<script>
import io from "socket.io-client";
import Player from "./components/Player.vue";
import Space from "./components/Space.vue";
import Pyramid from "./components/Pyramid.vue";

export default {
  name: "App",
  data: function () {
    var init_spaces = new Object;
    var i;
    for (i = 1; i <= 16; i++) {
      init_spaces[i] = {'id': i, 'camels': [], 'desert': 0};
    }
    return {
      registered: false,
      currentP: "",
      players: [],
      pName: "",
      addHuman: false,
      pID: "",
      spaces: init_spaces,
      init_spaces: init_spaces,
      actions: null,
    }
  },
  components: {
    Player,
    Space,
    Pyramid,
  },
  created() {
    this.connectWebsocket();
  },
  beforeUnmount() {
    this.disconnectWebsocket();
  },
  methods: {
    connectWebsocket() {
      this.socket = io("/message", {path: "/backend/socket.io"});
      this.socket.on("register", (message) => {
          console.log(message);
      });
      this.socket.on("notification", (message) => {
          console.log(message["content"]);
      });
      this.socket.on("info", (content) => {
          console.log(content);
          let type = content["type"]
          switch (type) {
            case "registration_result":
              this.register_confirm(content);
              break;
            case "players":
              this.update_player_info(content);
              break;
            case "board":
              this.update_board_info(content);
              break;
            case "reset":
              this.reset();
              break;
            case "action":
              this.actions = content;
              break;
          }
      });
      this.socket.on("player", (content) => {
          console.log(content);
          this.currentP = content;
      });
    },
    disconnectWebsocket() {
      if (this.socket) {
        this.socket.emit("disconnect");
        this.socket.disconnect();
      }
    },
    register: function(name, nPlayers) {
      if (this.socket) {
        this.socket.emit("register", name, nPlayers);
      } else {
        console.log(name, nPlayers);
      }
    },
    register_confirm(content) {
      if (content["registered"] == "True") {
        this.registered = true
        this.pName = content["player_name"]
        this.pId = content["player_id"]
      }
    },
    update_player_info(content) {
        this.players = content["Players"]
        this.currentP = content["currentP"]
        console.log(this.players)
    },
    next_player: function() {
      console.log("Next player")
      this.socket.emit("next_player");
    },
    start: function() {
      console.log("Game begins")
      this.socket.emit("start");
    },
    reset: function() {
      this.socket.emit("reset");
      this.spaces = this.init_spaces;
    },
    update_board_info(content) {
      this.spaces = content['spaces']
    }
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.container {
  display: flex;
}
.grade-board {
  display: flex;
  flex-direction: column;
}
.game-board {
  padding-top: 30px;
  padding-left: 30px;
  width: 650px;
  height: 650px;
  position: relative;
}
.pyramid {
  border: 1px solid black;
  height: 360px;
  width: 360px;
  background-color: #8b7355;
  position: absolute;
  top: 120px;
  left: 120px;
}
</style>

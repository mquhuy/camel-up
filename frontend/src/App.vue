<template>
  <div v-if="this.gameState == 'registration'" class="buttons">
    <div id="registration">
      <div class="human-player">
        <input type="checkbox" v-model="addHuman"> Include Human Player
        <input v-if="addHuman" v-model="pName" placeholder="Enter your name">
      </div>
      <input v-model.number="nP" type="number" placeholder="Number of bot players">
      <button @click="register(pName, nP)">Register</button>
    </div>
  </div>
  <div v-if="this.gameState == 'initialization'" class="buttons">
    <button @click="start">Start Game</button>
  </div>
  <div v-if="this.gameState == 'play'">
    <div class="container">
      <Board :tiles="this.bettingTiles"
             :spaces="this.spaces"
             :actions="this.actions"
             :inActive="!this.isCurrent || this.turnEnd" />
      <div class="grade-board">
        <div id="players" v-for="player in this.players" :key="player.id">
          <Player :player=player />
        </div>
      </div>
      <button :disabled="!isCurrent || turnEnd" @click="performMove({'action': 'roll'})">Roll</button>
    </div>
  </div>
  <div class="result" v-if="this.gameState == 'result'">
    <p>Final results</p>
    <div class="grade-board">
      <div id="players" v-for="player in this.results" :key="player.id">
        <Player :player=player />
      </div>
    </div>
    <button @click="reset">Replay</button>
    <button @click="new_game">New Game</button>
  </div>
</template>

<script>
import Player from "./components/Player";
import Board from "./components/board/Board";
import { mapState } from 'vuex';

export default {
  name: "App",
  computed: {
    isCurrent() {
      if (! this.gameState == "play" || this.id < 0) {
        return false;
      }
      const localPlayer = this.players.find(player => player.id == this.id);
      if (! localPlayer ) {
          return false;
      }
      return localPlayer.current;
    },
    ...mapState([
      "name",
      "id",
      "registered",
      "spaces",
      "players",
      "gameState",
      "actions",
      "bettingTiles",
      "results",
      "turnEnd",
    ]),
  },
  data() {
    return {
      "nP": 0,
      "addHuman": false,
      "pName": "",
    }
  },
  mounted() {
    this.$store.dispatch("sendCommand", {command: "reConnect",
                                         id: this.id, name: this.name});
  },
  methods: {
    start: function() {
      this.$store.dispatch("sendCommand", {command: "start"});
    },
    register: function(pName, nP) {
      this.$store.dispatch("sendCommand", {command: "register",
                                           name: pName,
                                           nP: nP});
    },
    reset: function() {
      this.$store.dispatch("sendCommand", {"command": "reset"});
    },
    new_game: function() {
      this.$store.dispatch("sendCommand", {"command": "new_game"});
    },
    performMove: function(params) {
      if (! this.isCurrent ) {
        console.log("Wait until your turn");
        return;
      }
     if ( this.turnEnd ) {
        return;
     }
     this.$store.dispatch("performMove", params);
    },
  },
  components: {
    Board,
    Player,
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
</style>

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
    <button @click="start">Start Game</button>
  </div>
  <div v-if="this.gameState == 'replay'" class="buttons">
    <button @click="start">Start Game</button>
  </div>
  <div v-if="this.gameState == 'play'">
    <div class="leg-betting-tiles">
      <LegBettingTile v-for="tile in this.bettingTiles" :key="tile.camel" :tile="tile"
                      @click="performMove({'action': 'bet-leg', 'camel': tile.camel})"/>
    </div>
    <div class="container">
      <div v-if="this.spaces" class="game-board">
        <Space v-for="space in this.spaces"
               :key="space.id"
               :space="space"
               @click="performMove({'action': 'dessert', 'space': space})"/>
        <div class="pyramid">
          <Pyramid :action="this.actions" :key="this.actions" />
        </div>
      </div>
      <div class="grade-board">
        <div id="players" v-for="player in this.players" :key="player.id">
          <Player :player=player />
        </div>
      </div>
      <button v-if="isCurrent" @click="roll">Roll</button>
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
import Player from "./components/Player.vue";
import Space from "./components/board/Space.vue";
import Pyramid from "./components/board/Pyramid.vue";
import LegBettingTile from "./components/board/LegBettingTile";
import { mapState } from 'vuex';

export default {
  name: "App",
  computed: {
    isCurrent() {
      if (! this.gameState == "play" || this.id < 0) {
        return false;
      }
      const localPlayer = this.players.find(player => player.id == this.id);
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
    if (this.id > 0) {
      this.$store.dispatch("sendCommand", {command: "reConnect",
                                           id: this.id});
    };
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
    roll: function() {
      this.$store.dispatch("sendAction", [0, 0, 1, ""]);
    },
    performMove: function(params) {
      if (! this.isCurrent ) {
        console.log("Wait until your turn");
        return;
      }
     this.$store.dispatch("performMove", params);
    },
  },
  components: {
    Player,
    Space,
    Pyramid,
    LegBettingTile,
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
.leg-betting-tiles {
  display: flex;
}
</style>

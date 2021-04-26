<template>
  <div v-if="this.gameState == 'registration'" class="buttons">
    <div id="registration">
      <input v-model="pName" placeholder="Enter your name" />
      <p>
        Number of players
        <input v-model.number="nPlayers" :min="0" type="number" />
      </p>
      <p>
        Number of bots
        <input v-model.number="nBots" :min="0" type="number" />
      </p>
      <button @click="register(pName, nPlayers, nBots)">Register</button>
    </div>
  </div>
  <div v-if="this.gameState == 'initialization'" class="buttons">
    <div class="join" v-if="!registered">
      <input v-model="pName" placeholder="Enter your name" />
      <button @click="register(pName, nPlayers, nBots)">Join</button>
    </div>
    <button v-if="!this.ready && registered" @click="start">Ready</button>
    <p v-if="this.ready">Waiting for other players</p>
  </div>
  <div v-if="this.gameState == 'play'">
    <div class="container">
      <Board />
      <div class="grade-board">
        <div id="players" v-for="player in this.players" :key="player.id">
          <Player :player="player" />
        </div>
      </div>
    </div>
  </div>
  <div class="result" v-if="this.gameState == 'result'">
    <p>Final results</p>
    <div class="grade-board">
      <div id="players" v-for="player in this.results" :key="player.id">
        <Player :player="player" />
      </div>
    </div>
    <button @click="reset">Replay</button>
    <button @click="new_game">New Game</button>
  </div>
</template>

<script>
import Player from "./components/Player";
import Board from "./components/board/Board";
import { mapState, mapActions } from "vuex";

export default {
  name: "App",
  computed: {
    ...mapState([
      "name",
      "id",
      "registered",
      "players",
      "gameState",
      "actions",
      "bettingTiles",
      "results",
      "turnEnd",
      "betDeck",
    ]),
  },
  data() {
    return {
      nBots: 0,
      nPlayers: 0,
      pName: "",
      ready: false,
    };
  },
  mounted() {
    this.$store.dispatch("sendCommand", {
      command: "reConnect",
      id: this.id,
      name: this.name,
    });
  },
  methods: {
    start: function () {
      this.$store.dispatch("sendCommand", { command: "start" });
      this.ready = true;
    },
    register: function (pName, nPlayers, nBots) {
      this.$store.dispatch("sendCommand", {
        command: "register",
        name: pName,
        nPlayers: nPlayers,
        nBots: nBots,
      });
    },
    reset: function () {
      this.$store.dispatch("sendCommand", { command: "reset" });
    },
    new_game: function () {
      this.$store.dispatch("sendCommand", { command: "new_game" });
    },
    ...mapActions(["performMove"]),
  },
  components: {
    Board,
    Player,
  },
};
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

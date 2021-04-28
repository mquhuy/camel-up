<template>
  <div v-if="this.gameState == 'registration'" class="grade-board">
    <div id="registration">
      <input :value="name" @input="updateName" placeholder="Enter your name" />
      <p>
        Number of players
        <input v-model.number="nPlayers" :min="0" type="number" />
      </p>
      <p>
        Number of bots
        <input v-model.number="nBots" :min="0" type="number" />
      </p>
      <button @click="register(name, nPlayers, nBots)">Register</button>
    </div>
  </div>
  <div v-if="this.gameState == 'initialization'" class="buttons">
    <div class="join" v-if="!registered">
      <input v-model="name" placeholder="Enter your name" />
      <button @click="register(name, nPlayers, nBots)">Join</button>
    </div>
    <button v-if="!ready && registered" @click="start">Ready</button>
    <p v-if="ready">Waiting for other players</p>
  </div>
  <div v-if="this.gameState == 'play'">
    <div class="container">
      <Board />
      <BettingDeck />
      <div class="grade-board">
        <div id="players" v-for="player in this.players" :key="player.id">
          <Player :player="player" />
        </div>
      </div>
    </div>
  </div>
  <div class="result" v-if="this.gameState == 'result'">
    <div class="grade-board">
    <p>Final results</p>
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
import BettingDeck from "./components/BettingDeck";
import { mapState, mapActions } from "vuex";

export default {
  name: "App",
  computed: {
    ...mapState([
      "id",
      "name",
      "registered",
      "players",
      "gameState",
      "actions",
      "bettingTiles",
      "results",
      "turnEnd",
      "betDeck",
      "ready",
    ]),
  },
  data() {
    return {
      nBots: 0,
      nPlayers: 0,
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
    register: function (name, nPlayers, nBots) {
      this.$store.dispatch("sendCommand", {
        command: "register",
        name: name,
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
    updateName (e) {
      this.$store.commit("UPDATE_NAME", e.target.value);
    },
    ...mapActions(["performMove"]),
  },
  components: {
    Board,
    BettingDeck,
    Player,
  },
};
</script>

<style lang=scss>
@import "../scss/_colors.scss";
body {
  background-color: $background;
  background-image: url("https://www.transparenttextures.com/patterns/tileable-wood-colored.png");
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.container {
  display: flex;
}
.grade-board {
  background-color: $white;
  padding: 15px;
  border-radius: 25px;
  display: flex;
  flex-direction: column;
}
</style>

<template>
  <div v-if="this.gameStage == 'initialization'" class="grade-board">
    <Register />
  </div>
  <div class="join" v-if="!registered">
    <input v-model="playerName" placeholder="Enter your name" />
    <input v-model="joinId" placeholder="Game Id" />
    <button @click="join(playerName, joinId, id)">Join</button>
  </div>
  <div v-if="this.gameStage == 'registration'" class="buttons">
    <button v-if="!ready && registered" @click="start">Ready</button>
    <p v-if="ready">Waiting for other players</p>
  </div>
  <div v-if="this.gameStage == 'play'">
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
  <div class="result" v-if="this.gameStage == 'result'">
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
import Register from "./components/Register";
import Player from "./components/Player";
import Board from "./components/board/Board";
import BettingDeck from "./components/BettingDeck";
import { mapState, mapActions } from "vuex";

export default {
  name: "App",
  computed: {
    ...mapState([
      "gameId",
      "id",
      "name",
      "registered",
      "players",
      "gameStage",
      "actions",
      "bettingTiles",
      "results",
      "turnEnd",
      "betDeck",
      "ready",
    ]),
  },
  data () {
    return {
      playerName: null,
      joinId: null,
    }
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
    reset: function () {
      this.$store.dispatch("sendCommand", { command: "reset" });
    },
    new_game: function () {
      this.$store.dispatch("sendCommand", { command: "new_game" });
    },
    join: function (name, gameId, playerId) {
      this.$store.dispatch("sendCommand", {
        command: "join",
        name: name,
        gameId: gameId,
        id: playerId,
      });
    },
    ...mapActions(["performMove"]),
  },
  components: {
    Register,
    Board,
    BettingDeck,
    Player,
  },
};
</script>

<style lang="scss">
@import "../scss/_colors.scss";
body {
  background-color: $background;
  background-image: url("../img/tileable-wood-colored.png");
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

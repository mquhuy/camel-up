<template>
  <div v-if="this.gameStage == 'initialization'" class="grade-board">
    <Register />
  </div>
  <div class="join" v-if="!registered">
    <input :value="name" @input="updateName" placeholder="Enter your name" />
    <input :value="gameId" @input="updateGameId" placeholder="Game Id" />
    <button @click="join(name, gameId)">Join</button>
  </div>
  <div v-if="this.gameStage == 'registration'" class="grade-board">
    <button v-if="!ready && registered" @click="start">Ready</button>
    <p v-if="ready">Waiting for other players. Use this game id to invite them: {{ gameId }}</p>
  </div>
  <div v-if="this.gameStage == 'play'">
    <div class="container">
      <Board />
      <BettingDeck />
      <div class="grade-board">
        <div class="players">
          <div v-for="player in this.players" :key="player.id">
          <Player :player="player" />
          </div>
        </div>
        <div class="end-game">
          <button @click="endGameClicked=true">End game</button>
          <div class="endGameBtn" v-if="endGameClicked">
            Are you sure to end game?
            <button @click="end_game()">Yes</button>
            <button @click="endGameClicked=false">No</button>
          </div>
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
    <button @click="end-game">New Game</button>
  </div>
</template>

<script>
import Register from "./components/Register";
import Player from "./components/Player";
import Board from "./components/board/Board";
import BettingDeck from "./components/BettingDeck";
import { mapState } from "vuex";

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
      endGameClicked: false,
    }
  },
  mounted() {
    this.$store.dispatch("sendCommand", {
      command: "reConnect",
    });
  },
  beforeUnmount() {
    this.$store.dispatch("sendCommand", {
      command: "disconnect_player",
    });
  },
  methods: {
    start: function () {
      this.$store.dispatch("sendCommand", { command: "start" });
    },
    updateName(e) {
      this.$store.commit("UPDATE_NAME", e.target.value);
    },
    updateGameId(e) {
      this.$store.commit("UPDATE_GAME_ID", e.target.value);
    },
    reset: function () {
      this.$store.dispatch("sendCommand", { command: "reset" });
    },
    join: function () {
      this.$store.dispatch("sendCommand", { command: "join" });
    },
    end_game: function () {
      this.$store.dispatch("sendCommand", { command: "end_game" });
    },
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
  justify-content: space-between;
  .players {
    display: flex;
    flex-direction: column;
  }
  .end-game {
    .endGameBtn {
      margin-top: 10px;
      button {
        margin: 0 1px;
      }
    }
  }
}
</style>

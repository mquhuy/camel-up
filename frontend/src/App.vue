<template>
  <div id="registration" v-if="!registered">
    <div class="human-player">
      <input type="checkbox" v-model="addHuman"> Include Human Player
      <input v-if="addHuman" v-model="pName" placeholder="Enter your name">
    </div>
    <input v-model.number="nP" type="number" placeholder="Number of bot players">
    <button v-on:click="register(pName, nP)">Register</button>
  </div>
  <div v-if="!this.gameOn" class="buttons">
      <button v-on:click="start">Start Game</button>
      <button v-on:click="next_player">End turn</button>
  </div>
  <div class="container">
    <div v-if="this.spaces" class="game-board">
      <Space v-for="space in this.spaces" :key="space.id" :space="space" />
      <div class="pyramid">
        <Pyramid :action_info="this.actions" :key="this.actions" />
      </div>
    </div>
    <div class="grade-board">
      <div id="players" v-for="player in this.players" :key="player.id">
        <Player :player=player />
      </div>
    </div>
  </div>
</template>

<script>
import Player from "./components/Player.vue";
import Space from "./components/board/Space.vue";
import Pyramid from "./components/board/Pyramid.vue";
import { mapState } from 'vuex';

export default {
  name: "App",
  computed: mapState([
      "registered",
      "spaces",
      "players",
      "gameOn",
      "actions",
  ]),
  data() {
    return {
      "nP": 0,
      "addHuman": false,
      "pName": "",
    }
  },
  methods: {
    start: function() {
      this.$store.dispatch("sendCommand", {command: "start"});
    },
    register: function(pName, nP) {
      this.$store.dispatch("sendCommand", {command: "register",
                                           name: pName,
                                           nP: nP});
    }
  },
  components: {
    Player,
    Space,
    Pyramid,
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

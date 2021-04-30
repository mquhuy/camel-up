<template>
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
    <button @click="register(name, nPlayers, nBots)">Create New Game</button>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "Register",
  computed: mapState(["name"]),
  data() {
    return {
      nBots: 0,
      nPlayers: 0,
    };
  },
  methods: {
    updateName(e) {
      this.$store.commit("UPDATE_NAME", e.target.value);
    },
    register: function (name, nPlayers, nBots) {
      this.$store.dispatch("sendCommand", {
        command: "register",
        name: name,
        nPlayers: nPlayers,
        nBots: nBots,
      });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../scss/_colors.scss";
.board {
  background-color: $white;
  padding: 15px;
  border-radius: 25px;
  display: flex;
  flex-direction: column;
}
</style>

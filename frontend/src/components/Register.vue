<template>
  <div class="currentPlayer">
    <h1 :playerName="playerName">{{ playerName }}</h1>
  </div>
  <!--<button v-on:click="playerName = current_player">Show player</button>-->
</template>

<script>
export default {
  name: "Player",
  props: {
    playerName: String
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  margin: 40px 0 0;
}
div {
  display: inline-block;
  margin: 0 10px;
}
</style>

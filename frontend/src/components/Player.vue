<template>
    <div v-if="playerId == currentP">
      <h1 :playerName="playerName" :points="points">{{ playerName }}: {{ points }}</h1>
    </div>
    <div v-if="playerId != currentP">
      <h3 :playerName="playerName" :points="points">{{ playerName }}: {{ points }}</h3>
    </div>
</template>

<script>
export default {
  name: "Player",
  props: {
    playerId: Number,
    playerName: String,
    currentP: Number,
    points: Number,
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

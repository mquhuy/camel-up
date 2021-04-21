<template>
    <div v-if="player.current">
      <h1>{{ player.name }}: {{ player.points }}</h1>
    </div>
    <div v-if="!player.current">
      <h3>{{ player.name }}: {{ player.points }}</h3>
    </div>
</template>

<script>
export default {
  name: "Player",
  props: ['player'],
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

<template>
  <div class="leg-betting-tile" :class="tile.color">
      <p class="card">{{ tile.card }}</p>
  </div>
</template>

<script>
export default {
  name: "LegBettingTile",
  props: ["tile"],
};
</script>

<style scoped>
.leg-betting-tile {
    border: 1px solid black;
    height: 200px;
    width: 150px;
}
.card {
    font-size: 80px;
    color: purple;
}
.green {
    background-color: green;
}
.blue {
    background-color: blue;
}
.yellow {
    background-color: yellow;
}
.white {
    background-color: white;
}
.orange {
    background-color: orange;
}
</style>

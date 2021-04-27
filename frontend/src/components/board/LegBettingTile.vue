<template>
    <div class="leg-betting-tile" :class="tile.camel" :disabled="inactive">
      <div class="card">
        <img class="camel-image" src="../../../img/camel.svg" />
        <p>{{ tile.bet }}</p>
      </div>
    </div>
</template>

<script>
export default {
  name: "LegBettingTile",
  props: ["tile", "inactive"],
};
</script>

<style scoped>
.leg-betting-tile {
  border: 1px solid black;
  height: 150px;
  width: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.card {
  font-size: 80px;
  color: purple;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.card p {
  margin: 0;
}
.camel-image {
  width: 60px;
  height: 50px;
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

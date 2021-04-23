<template>
    <div class="leg-betting-tile" :class="tile.camel" :disabled="inactive">
      <p class="card">{{ tile.bet }}</p>
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

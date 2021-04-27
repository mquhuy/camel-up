<template>
    <div class="leg-betting-tile" :class="tile.camel">
      <div class="card" :class="{active: tile.bet != 0}">
        <img class="camel-image" :class="tile.camel" src="../../../img/camel.svg" />
        <div v-if="tile.bet != 0" :class="tile.camel">{{ tile.bet }}</div>
      </div>
    </div>
</template>

<script>
export default {
  name: "LegBettingTile",
  props: ["tile", "inactive"],
};
</script>

<style lang=scss scoped>
.leg-betting-tile {
  border: 1px solid black;
  height: 150px;
  width: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.card {
  background-color: #c2a13e;
  background-image: url("../../../img/45-degree-fabric-dark.png");
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  width: 100%;
  height: 100%;
  div.green {
    color: green;
  }
  img.green {
    filter: invert(28%) sepia(99%) saturate(1117%) hue-rotate(90deg) brightness(96%) contrast(106%);
  }
  div.blue {
    color: blue;
  }
  img.blue {
    filter: invert(8%) sepia(100%) saturate(6389%) hue-rotate(246deg) brightness(103%) contrast(143%);
  }
  div.yellow {
    color: yellow;
  }
  img.yellow {
    filter: invert(100%) sepia(100%) saturate(1914%) hue-rotate(0deg) brightness(101%) contrast(104%);
  }
  div.white {
    color: white;
  }
  img.white {
    filter: invert(100%) sepia(0%) saturate(7485%) hue-rotate(159deg) brightness(105%) contrast(108%);
  }
  div.orange {
    color: orange;
  }
  img.orange {
    filter: invert(59%) sepia(70%) saturate(985%) hue-rotate(360deg) brightness(102%) contrast(105%);
  }
  img.camel-image {
    width: 60px;
    height: 50px;
  }
  div {
    margin: 0;
    width: 60%;
    border-radius: 50px;
    border: 5px solid;
    font-size: 50px;
  }
  &.active:hover {
    filter: invert(29%) brightness(122%) contrast(105%);
  }
}
</style>

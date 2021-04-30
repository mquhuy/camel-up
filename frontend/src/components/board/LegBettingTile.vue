<template>
  <div class="leg-betting-tile" :class="tile.camel">
    <div class="card" :class="{ active: tile.bet != 0 && actionable }">
      <img
        class="camel-image"
        :class="tile.camel"
        src="../../../img/camel.svg"
      />
      <div v-if="tile.bet != 0" :class="tile.camel">{{ tile.bet }}</div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "LegBettingTile",
  props: ["tile"],
  computed: mapGetters(["actionable"]),
};
</script>

<style lang="scss" scoped>
@import "../../../scss/_colors.scss";
.leg-betting-tile {
  border: none;
  height: 150px;
  width: 112px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.card {
  background-color: $leg-betting-bg;
  background-image: url("../../../img/45-degree-fabric-dark.png");
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  width: 100%;
  height: 100%;
  div.green {
    color: $green;
  }
  img.green {
    filter: $green-filter;
  }
  div.blue {
    color: $blue;
  }
  img.blue {
    filter: $blue-filter;
  }
  div.yellow {
    color: $yellow;
  }
  img.yellow {
    filter: $yellow-filter;
  }
  div.white {
    color: $white;
  }
  img.white {
    filter: $white-filter;
  }
  div.orange {
    color: $orange;
  }
  img.orange {
    filter: $orange-filter;
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
    background-color: $leg-betting-bg-hover;
  }
}
</style>

<template>
  <div class="board">
    <div class="leg-betting-tiles">
      <LegBettingTile
        v-for="tile in bettingTiles"
        :key="tile.camel"
        :tile="tile"
        @click="performMove({ action: 'bet-leg', camel: tile })"
      />
    </div>
    <div class="spaces">
      <Space v-for="space in spaces" :key="space.id" :space="space" />
      <div class="pyramid">
        <Pyramid />
      </div>
      <div class="hidden"></div>
    </div>
    <FinalBettingDeck />
  </div>
</template>

<script>
import Space from "./Space.vue";
import Pyramid from "./Pyramid.vue";
import LegBettingTile from "./LegBettingTile";
import FinalBettingDeck from "./FinalBettingDeck";
import { mapState, mapActions } from "vuex";
export default {
  name: "Board",
  computed: mapState(["spaces", "bettingTiles"]),
  components: {
    Space,
    Pyramid,
    LegBettingTile,
    FinalBettingDeck,
  },
  methods: mapActions(["performMove", "changeCurrentBetCamel"]),
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang=scss scoped>
@import "../../../scss/_colors.scss";
.board {
  padding-top: 30px;
  padding-left: 30px;
  width: 650px;
  height: 650px;
  position: relative;
  display: flex;
  flex-direction: column;
}
.spaces {
  position: relative;
}
.hidden {
  height: 600px;
  z-index: -1;
  visibility: hidden;
}
.pyramid {
  border: 1px solid $white-border;
  height: 360px;
  width: 360px;
  background-color: $brown;
  position: absolute;
  top: 120px;
  left: 120px;
}
.leg-betting-tiles {
  width: 600px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}
</style>

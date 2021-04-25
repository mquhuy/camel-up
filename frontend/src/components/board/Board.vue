<template>
  <div class="board">
    <div class="leg-betting-tiles">
      <LegBettingTile v-for="tile in tiles"
                      :key="tile.camel"
                      :tile="tile"
                      @click="performMove({'action': 'bet-leg', 'camel': tile})" />
    </div>
    <div class="spaces">
      <Space v-for="space in spaces"
             :key="space.id"
             :space="space"
             @click="performMove({'action': 'desert', 'space': space})" />
      <div class="pyramid">
        <Pyramid :action="actions" />
      </div>
      <div class="hidden"></div>
    </div>
    <p> Available betting cards </p>
    <div class="bet-deck">
      <div v-for="card in betDeck"
           class="deck-card"
           :key="card"
           :class="card"
           @click="performMove({'action': 'bet-winner', 'camel': card})"
           >
      </div>
    </div>
  </div>
</template>

<script>
import Space from "./Space.vue";
import Pyramid from "./Pyramid.vue";
import LegBettingTile from "./LegBettingTile";
export default {
  name: "Board",
  props: ["tiles", "spaces", "actions", "inActive", "betDeck"],
  components: {
    Space,
    Pyramid,
    LegBettingTile,
  },
  methods: {
    performMove: function(params) {
      if ( this.inActive ) {
        console.log("Wait until your turn");
        return;
      }
     this.$store.dispatch("performMove", params);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
  border: 1px solid black;
  height: 360px;
  width: 360px;
  background-color: #8b7355;
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
.bet-deck {
  display: flex;
}
.deck-card {
  margin: 10px;
  border: 1px solid black;
  height: 150px;
  width: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
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

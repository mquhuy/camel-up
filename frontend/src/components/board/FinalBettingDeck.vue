<template>
  <p>Your available betting cards</p>
  <div class="bet-deck">
    <div
      v-for="card in betDeck"
      class="deck-card"
      :key="card"
      :class="card"
      @mouseover="currentBetCamel = card"
      @mouseleave="currentBetCamel = null"
    >
      <div class="betting-choices" v-if="currentBetCamel == card && actionable">
        <button
          class="winner"
          @class="card"
          @click="performMove({ action: 'bet-winner', camel: currentBetCamel })"
        >
          Bet as final winner
        </button>
        <button
          class="loser"
          @class="card"
          @click="performMove({ action: 'bet-loser', camel: currentBetCamel })"
        >
          Bet as final loser
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
export default {
  name: "FinalBettingDeck",
  computed: {
    ...mapState(["betDeck"]),
    ...mapGetters(["actionable"]),
  },
  data: function () {
    return {
      currentBetCamel: null,
    };
  },
  methods: mapActions(["performMove"]),
};
</script>

<style scoped>
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
  background-image: url("../../../img/pyramid.svg");
  background-size: 100%;
  background-position: center;
  background-repeat: no-repeat;
}
.betting-choices {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 100%;
}
.betting-choices button {
  flex: 1;
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

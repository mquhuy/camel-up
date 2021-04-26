<template>
  <p>Available betting cards</p>
  <div class="bet-deck">
    <div
      v-for="card in betDeck"
      class="deck-card"
      :key="card"
      :class="card"
      @mouseover="changeCurrentBetCamel(card)"
      @mouseleave="changeCurrentBetCamel(null)"
    >
      <div class="betting-choices" v-if="currentBetCamel == card">
        <button
          class="winner"
          @click="
            performMove({ action: 'bet-winner', camel: currentBetCamel })
          "
        >
          Bet as final winner
        </button>
        <button
          class="loser"
          @click="
            performMove({ action: 'bet-loser', camel: currentBetCamel })
          "
        >
          Bet as final loser
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
  name: "FinalBettingDeck",
  computed: mapState(["currentBetCamel", "betDeck"]),
  methods: mapActions(["performMove", "changeCurrentBetCamel"]),
}
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
}
.betting-choices {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
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

<template>
  <div class="betting-deck">
    <div
      v-for="item in [lastBetWinner, lastBetLoser]"
      :key="item"
      class="card"
      :class="{ active: item != null }"
    >
      {{ item }}
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "BettingDeck",
  computed: mapState(["lastBetWinner", "lastBetLoser"]),
};
</script>

<style lang="scss" scoped>
@import "../../scss/_colors.scss";
.betting-deck {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 600px;
  margin-top: 190px;
  margin-right: 50px;
  .card {
    height: 220px;
    width: 150px;
    color: $white;
    background-color: $brown;
    display: flex;
    justify-content: center;
    align-items: center;
    background-image: url("../../img/null.png");
    background-size: auto 115px;
    background-repeat: no-repeat;
    background-position: center;
  }
  .active {
    font-size: 30px;
    background-repeat: repeat;
    background-image: url("../../img/45-degree-fabric-dark.png");
    border: 1px solid $white-border;
  }
}
</style>

<template>
  <div class="name" :class="{ active: player.current }">
    {{ player.name }}: {{ player.points }}
  </div>
  <div v-for="bet in bets" :key="bet.camel">
    <div v-for="card in bet.bet" :key="card" class="card" :class="bet.camel">
      {{ card }}
    </div>
  </div>
</template>

<script>
export default {
  name: "Player",
  props: ["player"],
  computed: {
    bets: function() {
      if (this.player.leg_bets) {
        return this.player.leg_bets.filter(bet => bet.bet.length > 0);
      }
      return [];
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang=scss scoped>
@import "../../scss/_colors.scss";
.name {
  margin: 20px 0 0;
  font-size: 30px;
}
.active {
  font-size: 80px;
}
div {
  display: inline-block;
}
.card {
  font-size: 40px;
  width: 20px;
  font-size: 25px;
  color: $white;
  margin-left: 5px;
}
.white {
  background-color: $white;
  color: $black !important;
  outline: 0.5px solid $black;
  outline-offset: -2px;
}
.orange {
  background-color: $orange;
}
.yellow {
  background-color: $yellow;
  color: $black !important;
}
.green {
  background-color: $green;
}
.blue {
  background-color: $blue;
}
</style>

<template>
    <div v-bind:class="{ active: player.current }">
        {{ player.name }}: {{ player.points }}
    </div>
       <div v-for="bet in bets" :key="bet.camel" :class="bet.camel" class="card">
            {{ bet.bet }}
        </div>
</template>

<script>
export default {
  name: "Player",
  props: ["player"],
  computed: {
    bets: function() {
      if (this.player.leg_bets) {
        return this.player.leg_bets.filter(bet => bet.bet > 0);
      }
      return [];
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.active {
  margin: 40px 0 0;
  font-size: 80px;
}
div {
  display: inline-block;
  margin: 0 10px;
  font-size: 40px;
}
.card {
  margin: 40px 0 0;
  width: 20px;
  font-size: 25px;
  color: white;
}
.white {
  background-color: white;
  color: black !important;
}
.orange {
  background-color: orange;
}
.yellow {
  background-color: yellow;
  color: black !important;
}
.green {
  background-color: green;
}
.blue {
  background-color: blue;
}
</style>

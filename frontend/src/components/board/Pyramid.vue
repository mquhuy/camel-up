<template>
  <div class="rolled-dice">
    <div
      v-for="roll in rollResults"
      :key="roll.die"
      class="rolled-die"
      :class="roll.die"
    >
      {{ roll.number }}
    </div>
  </div>
  <div v-if="actions && !actionable" class="action">
    <div v-if="actions.type != 'result'" class="info">
      {{ actions.player }} performs action {{ actions.action }}
    </div>
    <div v-if="actions.action == 'roll'" class="roll" :class="actions.camel">
      <div class="die">{{ actions.roll_num }}</div>
    </div>
    <div v-if="actions.type == 'result'" class="result">
      <div class="result-item">
        Camel {{ actions.winning_camel }} achieves the first place.
      </div>
      <div class="result-item">Player {{ actions.winning_player }} won.</div>
    </div>
  </div>
  <div class="roll-button" v-if="actionable">
    <p>Your turn</p>
    <button @click="performMove({ action: 'roll' })">
      Roll
      <img src="../../../img/pyramid-btn.png" />
    </button>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from "vuex";
export default {
  name: "Pyramid",
  computed: {
    ...mapState(["actions", "rollResults"]),
    ...mapGetters(["actionable"]),
  },
  methods: mapActions(["performMove"]),
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../scss/_colors.scss";
.info {
  height: 100px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  color: white;
}
.rolled-dice {
  display: flex;
  .rolled-die {
    width: 30px;
    height: 30px;
    margin: 10px 5px 0 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25em;
  }
}
.roll {
  width: 90px;
  height: 90px;
  color: $black;
  font-size: 3em;
  font-style: bold;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.action {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.roll-button {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.roll-button p {
  font-size: 4em;
  margin: 0;
}
.roll-button button {
  width: 120px;
  height: 120px;
  font-size: 2em;
  font-style: bold;
}
.roll-button button img {
  width: 80%;
  height: auto;
}
.die {
}
.white {
  background-color: $white;
}
.yellow {
  background-color: $yellow;
}
.blue {
  background-color: $blue;
  color: white;
}
.green {
  background-color: $green;
  color: white;
}
.orange {
  background-color: $orange;
}
div {
  display: inline-block;
  margin: 0 10px;
}
</style>

<template>
    <div v-if="action">
      <div class="info">
      {{ action.player }} performs action {{ action.action }}
      </div>
      <div v-if="action.action == 'roll'" class="roll" :class="action.camel">
        <div class="die">{{ action.roll_num }} </div>
      </div>
    </div>
</template>

<script>
export default {
  name: "Pyramid",
  props: ["action_info"],
  data () {
    return {
      action: this.action_info,
      roll: "roll",
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.info {
  height: 100px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  color: white;
}
.roll {
  width: 90px;
  height: 90px;
  color: black;
  font-size: 3em;
  font-style: bold;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.die {
}
.white {
  background-color: white;
}
.yellow {
  background-color: yellow;
}
.blue {
  background-color: blue;
  color: white;
}
.green {
  background-color: green;
  color: white;
}
.orange {
  background-color: orange;
}
div {
  display: inline-block;
  margin: 0 10px;
}
</style>

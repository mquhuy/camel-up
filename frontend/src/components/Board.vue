<template>
  <div class="board">
    <Space v-for="i in 16" :key="i" :info="spaces[i]"/>
    <div class="pyramid"></div>
  </div>
</template>

<script>
import Space from "./Space.vue";
export default {
  name: "Board",
  props: ["info"],
  watch: {
    info: function(){
      this.$emit('update:info', this.info)
    }
  },
  data() {
    return {
      spaces: this.info,
    }
  },
  components: {
    Space
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
</style>

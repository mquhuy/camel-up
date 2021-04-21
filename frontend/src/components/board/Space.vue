<template>
  <div :class="idClass" class="space">
    <div v-if="space.camels.length" class="camels">
      <div v-for="camel in space.camels " :key="camel" class="camel" :class="camel"></div>
    </div>
    <div v-if="space.desert != 0">
      <div class="desert">{{ space.desert }}</div>
      <div class="desert-owner">{{ space.desertP }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Space",
  props: [ "space"],
  data: function() {
    return {
      idClass: "id" + this.space.id,
    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.space {
  border: 1px solid black;
  height: 120px;
  width: 120px;
  background-color: #ffbf00;
  position: absolute;
}
.id1 {
  border-left: 5px dashed black;
  top: 0px;
  left: 240px;
}
.id2 {
  top: 0px;
  left: 360px;
}
.id3 {
  top: 0px;
  left: 480px;
}
.id4 {
  top: 120px;
  left: 480px;
}
.id5 {
  top: 240px;
  left: 480px;
}
.id6 {
  top: 360px;
  left: 480px;
}
.id7 {
  top: 480px;
  left: 480px;
}
.id8 {
  top: 480px;
  left: 360px;
}
.id9 {
  top: 480px;
  left: 240px;
}
.id10 {
  top: 480px;
  left: 120px;
}
.id11 {
  top: 480px;
  left: 0px;
}
.id12 {
  top: 360px;
  left: 0px;
}
.id13 {
  top: 240px;
  left: 0px;
}
.id14 {
  top: 120px;
  left: 0px;
}
.id15 {
  top: 0px;
  left: 0px;
}
.id16 {
  top: 0px;
  left: 120px;
}
.desert {
  width: 100%;
  height: 100%;
  background-color: grey;
  font-size: 5em;
}
.desert-owner  {
  width: 100%;
  height: 100%;
  background-color: red;
  color: white;
  font-size: 1.5em;
}
.camels {
  display: flex;
  flex-direction: column-reverse;
  justify-content: center;
}
.camel {
  width: 30px;
  height: 20px;
  margin: 0 auto;
}
.white {
  background-color: white;
}
.yellow {
  background-color: yellow;
}
.blue {
  background-color: blue;
}
.green {
  background-color: green;
}
.orange {
  background-color: orange;
}
</style>

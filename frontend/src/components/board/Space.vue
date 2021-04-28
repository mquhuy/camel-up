<template>
  <div
    :class="idClass"
    class="space"
    @mouseover="active = true"
    @mouseleave="active = false"
  >
    <div v-if="space.camels.length" class="camels">
      <img
        src="../../../img/camel-icon.svg"
        v-for="camel in space.camels"
        :key="camel"
        class="camel"
        :class="camel"
      />
    </div>
    <div v-if="space.desert != 0">
      <div class="desert">{{ space.desert }}</div>
      <div class="desert-owner">{{ space.desertP }}</div>
    </div>
    <div
      class="betting-choices"
      v-if="space.desertable && active && actionable"
    >
      <button
        :class="winner"
        @click="
          performMove({ action: 'desert', space_id: space.id, state: +1 })
        "
      >
        +1
      </button>
      <button
        class="loser"
        @click="
          performMove({ action: 'desert', space_id: space.id, state: -1 })
        "
      >
        -1
      </button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  name: "Space",
  props: ["space"],
  computed: mapGetters(["actionable"]),
  data: function () {
    return {
      idClass: "id" + this.space.id,
      active: false,
    };
  },
  methods: mapActions(["performMove"]),
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang=scss scoped>
@import "../../../scss/_colors.scss";
.space {
  border: 1px solid $white-border;
  height: 120px;
  width: 120px;
  background-image: url("../../../img/black-felt.png");
  background-color: $space_bg;
  position: absolute;
}
.id1 {
  border-left: 7px dashed $white-border;
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
  border-right: 7px dashed $white-border;
  top: 0px;
  left: 120px;
}
.desert {
  width: 100%;
  height: 100%;
  background-color: $desert_bg;
  font-size: 5em;
}
.desert-owner {
  width: 100%;
  height: 100%;
  background-color: $desert_owner_bg;
  color: white;
  font-size: 1.5em;
}
.camels {
  display: flex;
  flex-direction: column-reverse;
  justify-content: center;
  margin-top: 10px;
}
.camel {
  width: 40px;
  height: auto;
  margin: -5px auto;

  &.white {
    filter: $white-filter;
  }
  &.yellow {
    filter: $yellow-filter;
  }
  &.blue {
    filter: $blue-filter;
  }
  &.green {
    filter: $green-filter;
  }
  &.orange {
    filter: $orange-filter;
  }
}
.betting-choices {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  button {
    border: none;
    flex: 1;
    background-color: $space_bg_hover;
    &:hover {
      background-color: $space_bg;
    }
  }
}
</style>

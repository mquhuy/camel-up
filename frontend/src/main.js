import { createApp } from "vue";
import App from "./App.vue";
import VueSocketIO from "vue-3-socket.io";
import store from "./store";
import socket from "./socket";

const io = new VueSocketIO({
  debug: true,
  connection: socket,
  vuex: {
    store,
    actionPrefix: "SOCKET_",
    mutationPrefix: "SOCKET_",
  },
});

createApp(App).use(store).use(io).mount("#app");

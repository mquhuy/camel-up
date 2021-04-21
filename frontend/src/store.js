import { createStore } from "vuex";
import socket from "./socket";

var init_spaces = new Object();
var i;
for (i = 1; i <= 16; i++) {
  init_spaces[i] = {'id': i, 'camels': [], 'desert': 0};
}

const state = {
  isConnected: false,
  spaces: init_spaces,
  registered: false,
  currentP: "",
  players: [],
  pName: "",
  pID: "",
  actions: null,
  gameOn: false,
};

const mutations = {
  UPDATE_SPACES(state, payload) {
    state.spaces = payload;
  },
  UPDATE_PLAYERS(state, payload) {
    state.players = payload;
  },
  UPDATE_ACTIONS(state, payload) {
    state.actions = payload;
  },
};

const actions = {
  SOCKET_connect(state) {
    state.isConnected = true;
  },

  SOCKET_disconnect(state) {
    state.isConnected = false;
  },

  SOCKET_info(context, payload) {
    const type = payload.type;
    switch (type) {
      case "board":
        context.commit("UPDATE_SPACES", payload.spaces);
        break;
      case "players":
        context.commit("UPDATE_PLAYERS", payload.Players);
        break;
      case "action":
        context.commit("UPDATE_ACTIONS", payload);
        break;
      default:
        console.log(type);
    }
  },

  SOCKET_notification(content) {
    console.log(content);
  },

  SOCKET_register(content) {
    console.log(content);
  },

  sendCommand(_, details) {
    const command = details.command;
    socket.emit(command, details);
  },
};

const getters = {
    isConnected: state => state.isConnected,
};

const store = createStore({
  state,
  mutations,
  actions,
  getters,
});

export default store;

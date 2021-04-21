import { createStore } from "vuex";
import socket from "./socket";

const state = {
  isConnected: false,
  spaces: [],
  registered: false,
  players: [],
  pName: "",
  pID: "",
  actions: null,
  gameOn: false,
  bettingTiles: [],
};

const mutations = {
  START_GAME(state) {
    console.log("Starting the game")
    state.gameOn = true;
  },
  UPDATE_SPACES(state, payload) {
    state.spaces = payload;
  },
  UPDATE_PLAYERS(state, payload) {
    state.players = payload;
  },
  UPDATE_ACTIONS(state, payload) {
    state.actions = payload;
  },
  UPDATE_TILES(state, payload) {
    state.bettingTiles = payload;
  }
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
      case "game-start":
        context.commit("START_GAME");
        break;
      case "board":
        context.commit("UPDATE_SPACES", payload.spaces);
        break;
      case "players":
        context.commit("UPDATE_PLAYERS", payload.Players);
        break;
      case "action":
        context.commit("UPDATE_ACTIONS", payload);
        break;
      case "betting-tiles":
        context.commit("UPDATE_TILES", payload.leg_betting_tiles);
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

import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import socket from "./socket";

const getDefaultState = () => {
  return {
    gameId: null,
    isConnected: false,
    spaces: [],
    registered: false,
    name: "",
    id: -100,
    players: [],
    actions: null,
    gameStage: "initialization",
    results: {},
    bettingTiles: [],
    turnEnd: false,
    betDeck: [],
    rollResults: [],
    ready: false,
    lastBetWinner: null,
    lastBetLoser: null,
    errorLog: null,
  };
};

const state = getDefaultState();

const mutations = {
  RESET_ALL(state) {
    Object.assign(state, getDefaultState());
  },
  UPDATE_GAME_INFO(state, payload) {
    state.gameId = payload.game_id;
    state.gameStage = payload.game_stage;
  },
  UPDATE_GAME_RESULT(state, payload) {
    state.gameStage = payload.game_stage;
    state.results = payload.scoring;
  },
  UPDATE_SPACES(state, payload) {
    state.spaces = payload.spaces;
    state.lastBetWinner = payload.last_bet_winner;
    state.lastBetLoser = payload.last_bet_loser;
  },
  UPDATE_PLAYERS(state, payload) {
    state.players = payload.Players;
  },
  UPDATE_ACTIONS(state, payload) {
    state.actions = payload.action;
  },
  UPDATE_PLAYER_INFO(state, payload) {
    state.registered = payload.registered;
    state.name = payload.name;
    state.id = payload.id;
    state.bettingTiles = payload.leg_betting_tiles;
  },
  UPDATE_PERSONAL_INFO(state, payload) {
    state.betDeck = payload.bet_deck;
    state.ready = payload.ready;
  },
  UPDATE_TILES(state, payload) {
    state.bettingTiles = payload.leg_betting_tiles;
  },
  UPDATE_ALL(state, payload) {
    state.gameStage = payload.game_stage;
    state.spaces = payload.spaces;
    state.bettingTiles = payload.leg_betting_tiles;
    state.players = payload.Players;
    state.rollResults = payload.roll_results;
    state.lastBetWinner = payload.last_bet_winner;
    state.lastBetLoser = payload.last_bet_loser;
  },
  UPDATE_TURN_STATUS(state, payload) {
    state.turnEnd = payload;
  },
  UPDATE_NAME(state, payload) {
    state.name = payload;
  },
  UPDATE_GAME_ID(state, payload) {
    state.gameId = payload;
  },
  UPDATE_ERROR_LOG(state, payload) {
    state.errorLog = payload.error;
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
      case "all":
        context.commit("UPDATE_ALL", payload);
        break;
      case "action":
        context.commit("UPDATE_ACTIONS", payload);
        break;
      case "action-error":
        console.log(payload.error);
        context.commit("UPDATE_TURN_STATUS", false);
        break;
      case "action-success":
        context.commit("UPDATE_TURN_STATUS", false);
        break;
      case "betting-tiles":
        context.commit("UPDATE_TILES", payload);
        break;
      case "board":
        context.commit("UPDATE_SPACES", payload);
        break;
      case "game-start":
        context.commit("UPDATE_GAME_STAGE", payload);
        context.commit("UPDATE_TURN_STATUS", false);
        break;
      case "game-end-result":
        context.commit("UPDATE_GAME_RESULT", payload);
        break;
      case "game-deletion":
        context.commit("RESET_ALL");
        context.commit("UPDATE_ERROR_LOG", payload);
        break;
      case "players":
        context.commit("UPDATE_PLAYERS", payload);
        break;
      case "personal":
        context.commit("UPDATE_PERSONAL_INFO", payload);
        break;
      case "registration-success":
        context.commit("UPDATE_PLAYER_INFO", payload);
        context.commit("UPDATE_GAME_INFO", payload);
        break;
      case "registration-error":
        context.commit("RESET_ALL");
        context.commit("UPDATE_ERROR_LOG", payload);
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

  sendCommand({ state }, details) {
    const command = details.command;
    details.id = state.id;
    details.game_id = state.gameId;
    details.name = state.name;
    socket.emit(command, details);
  },

  performMove({ dispatch }, params) {
    const action = params.action;
    switch (action) {
      case "bet-leg":
        dispatch("legBet", params.camel);
        break;
      case "desert":
        dispatch("sendAction", [4, params.space_id, params.state, ""]);
        break;
      case "roll":
        dispatch("sendAction", [0, 1, 1, ""]);
        break;
      case "bet-winner":
        dispatch("sendAction", [2, 1, 1, params.camel]);
        break;
      case "bet-loser":
        dispatch("sendAction", [3, 1, 1, params.camel]);
        break;
    }
  },

  legBet({ state, dispatch }, camel) {
    if (!state.bettingTiles) {
      return;
    }
    if (camel.bet == 0) {
      console.log("All cards in this tile were taken.");
      return;
    }
    dispatch("sendAction", [1, 0, 0, camel.camel]);
  },

  sendAction({ state, dispatch, commit }, actions) {
    if (!getters.isCurrent) {
      console.log("Wait until your turn");
      return;
    }
    if (state.turnEnd) {
      return;
    }
    commit("UPDATE_TURN_STATUS", true);
    dispatch("sendCommand", { command: "action_choice", actions: actions });
  },
};

const getters = {
  isConnected: (state) => state.isConnected,
  isCurrent(state) {
    if (!state.gameStage == "play" || state.id == -100) {
      return false;
    }
    const localPlayer = state.players.find((player) => player.id == state.id);
    if (!localPlayer) {
      return false;
    }
    return localPlayer.current;
  },
  actionable(state, getters) {
    return getters.isCurrent && !state.turnEnd;
  },
};

const store = createStore({
  state,
  mutations,
  actions,
  getters,
  plugins: [createPersistedState()],
});

export default store;

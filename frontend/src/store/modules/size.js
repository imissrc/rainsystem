const state = {
  window: {
    width: document.documentElement.clientWidth,
    height: document.documentElement.clientHeight
  }
}

const mutations = {
  SET_WINDOW_SIZE: (state, window) => {
    state.window = window
  }
}

const actions = {
  setWindowSize({ commit }, window) {
    return new Promise((resolve, reject) => {
      commit('SET_WINDOW_SIZE', window)
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

import { login, logout } from '@/api/login'
import {
  getUserName,
  setUserName,
  removeUserName,
  getLoginState,
  setLoginState,
  removeLoginState
} from '@/utils/auth'
import { resetRouter } from '@/router'

const state = {
  username: getUserName(),
  loginState: getLoginState()
}

const mutations = {
  SET_USER_NAME: (state, username) => {
    state.username = username
  },
  SET_LOGIN_STATE: (state, loginState) => {
    state.loginState = loginState
  }
}

const actions = {
  // user login
  loginAct({ commit }, info) {
    return new Promise((resolve, reject) => {
      login({ username: info.username.trim(), password: info.password.trim() }).then(res => {
        if (res.code === 200) {
          commit('SET_USER_NAME', info.username)
          commit('SET_LOGIN_STATE', true)
          setUserName(info.username)
          setLoginState(true)
          resolve()
        }
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getLoginState({ username: state.username.trim() }).then(res => {
        if (res.code !== 200) {
          reject('Verification failed, please Login again.')
        } else {
          if (res.data === true) {
            commit('SET_USER_NAME', state.username)
            commit('SET_LOGIN_STATE', true)
            removeUserName()
            removeLoginState()
            resolve()
          }
        }
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logoutAct({ commit, state, dispatch }) {
    return new Promise((resolve, reject) => {
      logout({ username: state.username }).then(res => {
        commit('SET_USER_NAME', '')
        commit('SET_LOGIN_STATE', '')
        removeUserName()
        removeLoginState()
        resetRouter()

        // reset visited views and cached views
        // to fixed https://github.com/PanJiaChen/vue-element-admin/issues/2485
        dispatch('tagsView/delAllViews', null, { root: true })

        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetCurrentUserName({ commit }, username) {
    return new Promise(resolve => {
      commit('SET_USER_NAME', username)
      setUserName(username)
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

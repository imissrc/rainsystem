import {isLogin, login, logout} from '@/api/login'
import {
  getUserName,
  setUserName,
  removeUserName,
} from '@/utils/auth'
import router, { resetRouter } from '@/router'

const state = {
  username: getUserName(),
  roles: []
}

const mutations = {
  SET_USER_NAME: (state, username) => {
    state.username = username
  },
}

const actions = {
  // user login
  loginAct({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(res => {
        if (res.code === 200) {

          commit('SET_USER_NAME', username)
          commit('SET_IS_LOGIN', res.data.avatar)
          // setToken(res.data.token)
          // setInfoId(res.data.infoId)
          // setLoginName(loginName)
          // setAvatar(res.data.avatar)
          setUserName(res.data.username)
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
      isLogin().then(res => {
        if (res.code !== 200) {
          reject('Verification failed, please Login again.')
        } else {
          if (res.data.isLogin === true) {
            commit('SET_USER_NAME', res.data.username)
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
      logout().then(res => {

        commit('SET_USER_NAME', '')

        removeUserName()

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

import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export function register(data) {
  return request({
    url: '/register',
    method: 'post',
    data
  })
}

export function logout(params) {
  return request({
    url: '/logout',
    method: 'get',
    params: params
  })
}

export function findPassword(data) {
  return request({
    url: '/findPassword',
    method: 'post',
    data
  })
}

export function changePassword(data) {
  return request({
    url: '/changePassword',
    method: 'post',
    data
  })
}

export function getLoginState(params) {
  return request({
    url: '/getLoginState',
    method: 'get',
    params
  })
}

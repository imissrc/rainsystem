import request from '@/utils/request'

export function login (data) {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export function register (data) {
  return request({
    url: '/register',
    method: 'post',
    data
  })
}

export function logout () {
  return request({
    url: '/logout',
    method: 'get'
  })
}

export function findPassword (data) {
  return request({
    url: '/findPassword',
    method: 'post',
    data
  })
}

export function changePassword (data) {
  return request({
    url: '/changePassword',
    method: 'post',
    data
  })
}

export function getUserInfo (params) {
  return request({
    url: '/getUserInfo',
    method: 'get',
    params
  })
}

export function isLogin (params) {
  return request({
    url: 'isLogin',
    method: 'get',
    params
  })
}
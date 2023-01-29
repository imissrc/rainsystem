import request from '@/utils/request'

export function saveHistory () {
  return request({
    url: '/history/saveHistory',
    methid: 'get'
  })
}

export function getHistory () {
  return request({
    url: '/history/getHistory',
    methid: 'get'
  })
}

export function getHistoryTable (params) {
  return request({
    url: '/history/getHistoryTable',
    methid: 'get',
    params
  })
}

export function delHistory (params) {
  return request({
    url: 'history/delHistory',
    method: 'get',
    params
  })
}

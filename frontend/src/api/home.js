import request from '@/utils/request'

export function uploadFile (data) {
  return request({
    url: '/home/uploadFile',
    method: 'post',
    data
  })
}

export function runPredictFile () {
  return request({
    url: '/home/runPredictFile',
    method: 'get'
  })
}

export function uploadImage (data) {
  return request({
    url: '/home/uploadImage',
    method: 'post',
    data
  })
}

export function uploadManual (data) {
  return request({
    url: '/home/uploadManual',
    method: 'post',
    data
  })
}

export function home (params) {
  return request({
    url: '/home',
    method: 'get',
    params
  })
}

export function stopPredictFile () {
  return request({
    url: '/home/stopPredictFile',
    method: 'get'
  })
}

export function readyImages () {
  return request({
    url: '/home/readyImages',
    method: 'get'
  })
}

export function downloadData () {
  return request({
    url: '/home/downloadData',
    method: 'get'
  })
}

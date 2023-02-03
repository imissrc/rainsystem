import request from '@/utils/request'

export function uploadImagesAndRestore(data) {
  return request({
    url: '/uploadImagesAndRestore',
    method: 'post',
    data
  })
}

export function getDetailByTaskHistoryId(params) {
  return request({
    url: 'getDetailByTaskHistoryId',
    method: 'get',
    params: params
  })
}

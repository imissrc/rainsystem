import Request from '@/utils/request'
export const resourceUrl = 'https://self.brain-intelligence.cn'

export const addImage = data => Request.post(resourceUrl + '/resource/addImage', data)

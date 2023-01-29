const Mock = require('mockjs')
//const returnImg = function(){
//    return {'url' : '../.././assets/logo.png','code' : 200, 'status' : 1}
//}
const returnImg = function(){
    return {'code' : 200, 'result' : 1, 'image' : 'https://image.baidu.com/search/detail?ct=503316480&z=0&ipn=d&word=%E9%A3%8E%E6%99%AF&hs=0&pn=0&spn=0&di=53900&pi=0&rn=1&tn=baiduimagedetail&is=0%2C0&ie=utf-8&oe=utf-8&cl=2&lm=-1&cs=2641362231%2C3822011310&os=3999166766%2C1603520716&simid=2641362231%2C3822011310&adpicid=0&lpn=0&ln=30&fr=ala&fm=&sme=&cg=&bdtype=0&oriquery=%E9%A3%8E%E6%99%AF&objurl=https%3A%2F%2Fgimg2.baidu.com%2Fimage_search%2Fsrc%3Dhttp%3A%2F%2Fup.enterdesk.com%2Fedpic%2F4f%2F9e%2F7e%2F4f9e7e627c6d78884da8ac4a5a442ce8.jpg%26refer%3Dhttp%3A%2F%2Fup.enterdesk.com%26app%3D2002%26size%3Df9999%2C10000%26q%3Da80%26n%3D0%26g%3D0n%26fmt%3Djpeg%3Fsec%3D1636603379%26t%3De26d4fe89e435275dbecc067587026c2&fromurl=ippr_z2C%24qAzdH3FAzdH3Fooo_z%26e3Bjgpj61jfh_z%26e3Bv54AzdH3FktzitAzdH3F9abdn_z%26e3Bip4s&gsm=1&islist=&querylist=\n'}
}
const returnVideo = function(){
    return {'code' : 200, 'result' : 1, 'video' : 'https://image.baidu.com/search/detail?ct=503316480&z=0&ipn=d&word=%E9%A3%8E%E6%99%AF&hs=0&pn=0&spn=0&di=53900&pi=0&rn=1&tn=baiduimagedetail&is=0%2C0&ie=utf-8&oe=utf-8&cl=2&lm=-1&cs=2641362231%2C3822011310&os=3999166766%2C1603520716&simid=2641362231%2C3822011310&adpicid=0&lpn=0&ln=30&fr=ala&fm=&sme=&cg=&bdtype=0&oriquery=%E9%A3%8E%E6%99%AF&objurl=https%3A%2F%2Fgimg2.baidu.com%2Fimage_search%2Fsrc%3Dhttp%3A%2F%2Fup.enterdesk.com%2Fedpic%2F4f%2F9e%2F7e%2F4f9e7e627c6d78884da8ac4a5a442ce8.jpg%26refer%3Dhttp%3A%2F%2Fup.enterdesk.com%26app%3D2002%26size%3Df9999%2C10000%26q%3Da80%26n%3D0%26g%3D0n%26fmt%3Djpeg%3Fsec%3D1636603379%26t%3De26d4fe89e435275dbecc067587026c2&fromurl=ippr_z2C%24qAzdH3FAzdH3Fooo_z%26e3Bjgpj61jfh_z%26e3Bv54AzdH3FktzitAzdH3F9abdn_z%26e3Bip4s&gsm=1&islist=&querylist=\n'}
}
const returnCode = function(){
    return {'code' : 200, 'data' : 'test.jpg'}
}
Mock.mock('/api/uploadImage', 'post', returnCode)
Mock.mock('/api/queryImageTaskResult', 'post', returnImg)
Mock.mock('/api/uploadVideo', 'post', returnCode)
Mock.mock('/api/queryVideoTaskResult', 'post', returnVideo)
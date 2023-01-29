import Vue from 'vue'
import videoOCR from './videoOCR.vue'
import VueAxios from 'vue-axios'
import axios from 'axios'
import Video from 'video.js'
import 'video.js/dist/video-js.css'
//import '../.././mock'
Vue.prototype.$axios = axios
Vue.prototype.$video = Video
Vue.use(VueAxios, axios)
axios.defaults.baseURL = '/'
Vue.config.productionTip = false

new Vue({
    el: '#videoOCR',
    render: h => h(videoOCR)
})
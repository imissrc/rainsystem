import Vue from 'vue'
import videoEnhance from './videoEnhance.vue'
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
    el: '#videoEnhance',
    render: h => h(videoEnhance)
})
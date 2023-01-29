import Vue from 'vue'
import imageOCR from './imageOCR.vue'
import VueAxios from 'vue-axios'
import axios from 'axios'
//import '../.././mock'
Vue.prototype.$axios = axios
Vue.use(VueAxios, axios)
axios.defaults.baseURL = '/'
Vue.config.productionTip = false

new Vue({
    el: '#imageOCR',
    render: h => h(imageOCR)
})

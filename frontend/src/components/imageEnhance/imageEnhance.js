import Vue from 'vue'
import imageEnhance from './imageEnhance.vue'
import VueAxios from 'vue-axios'
import axios from 'axios'
//import '../.././mock'
Vue.prototype.$axios = axios
Vue.use(VueAxios, axios)
var instance = axios.create({
    baseURL: '/',
    timeout: 50000,
    headers:{"Content-Type": "multipart/form-data"},
});
axios.defaults.baseURL = '/'
Vue.config.productionTip = false
Vue.prototype.instance=instance;

new Vue({
    el: '#imageEnhance',
    render: h => h(imageEnhance)
})

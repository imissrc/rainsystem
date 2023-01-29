import Vue from 'vue'
import App from './App.vue'
Vue.config.productionTip = false
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import router from './router'
import { Icon } from 'ant-design-vue'
import axios from 'axios'
import store from "@/store";

Vue.use(Icon)
Vue.use(ElementUI)

import '@/icons' // icon

// 将axios对象强行添加到Vue类型的原型对象中
// 结果：
// 在所有组件中都可以用this.axios.get()发送请求
Vue.prototype.axios = axios

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

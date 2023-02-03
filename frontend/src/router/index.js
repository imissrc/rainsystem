import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/views/login/login'
import Register from '@/views/login/register'
import FindPassword from '@/views/login/findPassword'
import ChangePassword from '@/views/login/changePassword'

Vue.use(Router)

import Layout from '@/layout'

// 代表那些不需要动态判断权限的路由，如登录页、404、等通用页面。
export const constantRoutes = [
  {
    path: '/',
    redirect: '/login',
    hidden: true
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    hidden: true
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    hidden: true
  },
  {
    path: '/findPassword',
    name: 'FindPassword',
    component: FindPassword,
    hidden: true
  },
  {
    path: '/changePassword',
    name: 'ChangePassword',
    component: ChangePassword,
    hidden: true
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    redirect: '/dashboard/index',
    component: Layout,
    children: [
      {
        path: 'index',
        component: () => import('@/views/dashboard/index'),
        meta: {
          title: '首页',
          icon: 'dashboard'
        }
      }
    ]
  },
  {
    path: '/derain',
    name: 'Derain',
    component: Layout,
    redirect: '/derain/image',
    meta: {
      title: '图像/视频去雨',
      icon: 'documentation'
    },
    children: [
      {
        path: 'image',
        name: 'ImageDerain',
        component: () => import('@/views/derain/imageDerain'),
        meta: {
          title: '图像去雨'
        }
      },
      {
        path: 'video',
        name: 'VideoDerain',
        component: () => import('@/views/derain/videoDerain'),
        meta: {
          title: '视频去雨'
        }
      }
    ]
  },
  {
    path: '/history',
    name: 'history',
    component: Layout,
    redirect: '/history/image',
    meta: {
      title: '图像/视频历史记录',
      icon: 'documentation'
    },
    children: [
      {
        path: 'image',
        name: 'HistoryImageDerain',
        component: () => import('@/views/history/imageDerain'),
        meta: {
          title: '图像去雨历史记录'
        }
      },
      {
        path: 'video',
        name: 'HistoryVideoDerain',
        component: () => import('@/views/history/videoDerain'),
        meta: {
          title: '视频去雨历史记录'
        }
      }
    ]
  }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/v+ue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router

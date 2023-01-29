import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/login/Login'
import Register from '@/components/login/Register'
import FindPassword from '@/components/login/FindPassword'
import ChangePassword from '@/components/login/ChangePassword'

Vue.use(Router)

import Layout from '@/layout'

// 代表那些不需要动态判断权限的路由，如登录页、404、等通用页面。
export const constantRoutes = [
  {
    path: '/',
    name: 'Login',
    component: Login,
    meta: {
      keeplive: false
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    redirect: '/dashboard/index',
    component: Layout,
    children: [
      {
        path: 'index',
        component: () => import('@/components/dashboard/index'),
        meta: {
          title: '首页',
          icon: 'dashboard'
        }
      }
    ]
  },
  {
    path: '/derain',
    name: 'derain',
    component: Layout,
    children: [
        {
        path: 'index',
        component: () => import('@/components/dashboard/index'),
        meta: {
          title: '首页',
          icon: 'dashboard'
        }
      }
    ]
  },
  {
    path: '/history',
    name: 'manual',
    component: () => import('@/components/history/history'),
    meta: {
      keeplive: false
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      keeplive: false
    }
  },
  {
    path: '/findPassword',
    name: 'FindPassword',
    component: FindPassword,
    meta: {
      keeplive: false
    }
  },
  {
    path: '/changePassword',
    name: 'ChangePassword',
    component: ChangePassword,
    meta: {
      keeplive: false
    }
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
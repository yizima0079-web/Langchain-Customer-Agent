import { createRouter, createWebHistory } from 'vue-router'

/** 路由表：登录页 + 后台布局（含子路由） */
const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录' },
  },
  {
    path: '/',
    component: () => import('@/views/layout/index.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '数据统计' },
      },
      {
        path: 'category',
        name: 'category',
        component: () => import('@/views/category/index.vue'),
        meta: { title: '分类管理' },
      },
      {
        path: 'product',
        name: 'product',
        component: () => import('@/views/product/index.vue'),
        meta: { title: '商品管理' },
      },
      {
        path: 'banner',
        name: 'banner',
        component: () => import('@/views/banner/index.vue'),
        meta: { title: '轮播图管理' },
      },
      {
        path: 'order',
        name: 'order',
        component: () => import('@/views/order/index.vue'),
        meta: { title: '订单管理' },
      },
      {
        path: 'user',
        name: 'user',
        component: () => import('@/views/user/index.vue'),
        meta: { title: '用户管理' },
      },
      {
        path: 'knowledge',
        name: 'knowledge',
        component: () => import('@/views/knowledge/index.vue'),
        meta: { title: '知识库管理' },
      },
      {
        path: 'chat',
        name: 'chat',
        component: () => import('@/views/chat/index.vue'),
        meta: { title: 'AI 客服调试' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 登录守卫：未登录跳转到登录页
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router

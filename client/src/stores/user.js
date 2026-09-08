import { defineStore } from 'pinia'
import { login as loginApi } from '@/api'

/** 用户状态仓库：管理登录态与用户信息 */
export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user') || 'null'),
  }),
  getters: {
    isLogin: (state) => !!state.token,
  },
  actions: {
    /** 登录：调用接口并持久化 token 与用户信息 */
    async login(payload) {
      const data = await loginApi(payload)
      this.token = data.access_token
      this.user = data.user
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
    },
    /** 退出登录：清空本地状态 */
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
  },
})

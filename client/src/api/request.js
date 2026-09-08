import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

/** Axios 实例：统一注入 token、拦截响应 */
const service = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
})

// 请求拦截：携带 JWT
service.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截：统一解包 { code, message, data }
service.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code !== 0) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message))
    }
    return res.data
  },
  (error) => {
    // 401 未登录：清空并跳转登录
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }
    const msg = error.response?.data?.detail || error.message || '网络错误'
    ElMessage.error(msg)
    return Promise.reject(error)
  },
)

export default service

import request from './request'

/** 认证 */
export const login = (data) => request.post('/auth/login', data)
export const getMe = () => request.get('/auth/me')

/** 用户管理 */
export const getUsers = (params) => request.get('/users', { params })
export const updateUser = (id, data) => request.put(`/users/${id}`, data)
export const deleteUser = (id) => request.delete(`/users/${id}`)

/** 分类管理 */
export const getCategories = () => request.get('/categories')
export const createCategory = (data) => request.post('/categories', data)
export const updateCategory = (id, data) => request.put(`/categories/${id}`, data)
export const deleteCategory = (id) => request.delete(`/categories/${id}`)

/** 商品管理 */
export const getProducts = (params) => request.get('/products', { params })
export const createProduct = (data) => request.post('/products', data)
export const updateProduct = (id, data) => request.put(`/products/${id}`, data)
export const deleteProduct = (id) => request.delete(`/products/${id}`)

/** 轮播图管理 */
export const getBanners = (onlyActive = false) =>
  request.get('/banners', { params: { only_active: onlyActive } })
export const createBanner = (data) => request.post('/banners', data)
export const updateBanner = (id, data) => request.put(`/banners/${id}`, data)
export const deleteBanner = (id) => request.delete(`/banners/${id}`)

/** 订单管理 */
export const getOrders = (params) => request.get('/orders', { params })
export const updateOrderStatus = (id, status) => request.put(`/orders/${id}/status`, { status })

/** 数据统计 */
export const getStatsOverview = () => request.get('/stats/overview')
export const getSalesTrend = () => request.get('/stats/sales-trend')
export const getOrderStatus = () => request.get('/stats/order-status')
export const getCategoryStats = () => request.get('/stats/category')

/** 知识库 */
export const getKnowledge = () => request.get('/knowledge')
export const deleteKnowledge = (id) => request.delete(`/knowledge/${id}`)
export const uploadKnowledge = (file) => {
  const form = new FormData()
  form.append('file', file)
  return request.post('/knowledge', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

/** AI 客服 */
export const chat = (data) => request.post('/chat', data)
export const getChatHistory = (sessionId) => request.get('/chat/history', { params: { session_id: sessionId } })

/** 图片上传 */
export const uploadImage = (file, category = 'common') => {
  const form = new FormData()
  form.append('file', file)
  return request.post('/upload', form, {
    params: { category },
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

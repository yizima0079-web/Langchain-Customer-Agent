// pages/product/product.js 商品详情
const api = require('../../utils/api')

Page({
  data: {
    id: null,
    product: null,
  },

  onLoad(options) {
    this.setData({ id: options.id })
    this.loadProduct()
  },

  /** 加载商品详情 */
  loadProduct() {
    api.get('/products/' + this.data.id).then((res) => {
      res.cover_image = api.fullUrl(res.cover_image)
      this.setData({ product: res })
      wx.setNavigationBarTitle({ title: res.name })
    })
  },

  /** 校验登录，未登录跳转登录页 */
  ensureLogin() {
    if (!wx.getStorageSync('token')) {
      wx.navigateTo({ url: '/pages/mine/mine' })
      return false
    }
    return true
  },

  /** 加入购物车 */
  addCart() {
    if (!this.ensureLogin()) return
    api.post('/cart', { product_id: Number(this.data.id), quantity: 1 }).then(() => {
      wx.showToast({ title: '已加入购物车', icon: 'success' })
    })
  },

  /** 立即购买 */
  buyNow() {
    if (!this.ensureLogin()) return
    const items = JSON.stringify([{ product_id: Number(this.data.id), quantity: 1 }])
    wx.navigateTo({ url: '/pages/order/order?items=' + encodeURIComponent(items) })
  },
})

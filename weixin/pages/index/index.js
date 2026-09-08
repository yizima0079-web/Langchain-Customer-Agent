// pages/index/index.js 商城首页
const api = require('../../utils/api')

Page({
  data: {
    banners: [],
    categories: [],
    products: [],
    activeCategory: null,
  },

  onLoad() {
    this.loadBanners()
    this.loadCategories()
    this.loadProducts()
  },

  onShow() {
    if (this.getTabBar()) this.getTabBar().setData({ selected: 0 })
  },

  onPullDownRefresh() {
    this.loadBanners()
    this.loadCategories()
    this.loadProducts(this.data.activeCategory)
    wx.stopPullDownRefresh()
  },

  /** 加载顶部轮播图（仅启用项） */
  loadBanners() {
    api.get('/banners', { only_active: true }).then((res) => {
      const banners = res.map((b) => ({ ...b, image: api.fullUrl(b.image) }))
      this.setData({ banners })
    })
  },

  /** 加载分类 */
  loadCategories() {
    api.get('/categories').then((res) => {
      this.setData({ categories: res })
    })
  },

  /** 加载商品（可按分类过滤） */
  loadProducts(categoryId) {
    const params = { page: 1, size: 50, only_online: true }
    if (categoryId) params.category_id = categoryId
    api.get('/products', params).then((res) => {
      const items = res.items.map((p) => ({ ...p, cover_image: api.fullUrl(p.cover_image) }))
      this.setData({ products: items })
    })
  },

  /** 点击分类 */
  onCategoryTap(e) {
    const id = e.currentTarget.dataset.id
    this.setData({ activeCategory: id })
    this.loadProducts(id)
  },

  /** 查看全部 */
  onAllTap() {
    this.setData({ activeCategory: null })
    this.loadProducts()
  },

  /** 进入商品详情 */
  onProductTap(e) {
    wx.navigateTo({ url: '/pages/product/product?id=' + e.currentTarget.dataset.id })
  },
})

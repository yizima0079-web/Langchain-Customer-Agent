// pages/cart/cart.js 购物车
const api = require('../../utils/api')

Page({
  data: {
    items: [],
    total: '0.00',
  },

  onShow() {
    if (this.getTabBar()) this.getTabBar().setData({ selected: 2 })
    if (wx.getStorageSync('token')) {
      this.loadData()
    } else {
      this.setData({ items: [], total: '0.00' })
    }
  },

  /** 加载购物车 */
  loadData() {
    api.get('/cart').then((res) => {
      const items = res.map((i) => ({
        ...i,
        product_image: api.fullUrl(i.product_image),
        checked: true,
      }))
      this.setData({ items })
      this.calcTotal()
    })
  },

  /** 计算勾选商品总价 */
  calcTotal() {
    const total = this.data.items
      .filter((i) => i.checked)
      .reduce((sum, i) => sum + i.price * i.quantity, 0)
    this.setData({ total: total.toFixed(2) })
  },

  /** 勾选/取消勾选 */
  onCheck(e) {
    const idx = e.currentTarget.dataset.index
    const items = this.data.items
    items[idx].checked = !items[idx].checked
    this.setData({ items })
    this.calcTotal()
  },

  /** 修改数量 */
  changeQty(e) {
    const { index, delta } = e.currentTarget.dataset
    const item = this.data.items[index]
    const quantity = item.quantity + Number(delta)
    if (quantity < 1) return
    api.put('/cart/' + item.id, { quantity }).then(() => this.loadData())
  },

  /** 删除购物车项 */
  delItem(e) {
    api.del('/cart/' + e.currentTarget.dataset.id).then(() => this.loadData())
  },

  /** 结算 */
  checkout() {
    if (!this.data.items.filter((i) => i.checked).length) {
      wx.showToast({ title: '请先勾选商品', icon: 'none' })
      return
    }
    wx.navigateTo({ url: '/pages/order/order?from=cart' })
  },
})

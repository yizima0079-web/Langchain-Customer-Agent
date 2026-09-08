// pages/mine/mine.js 个人中心（登录 / 订单入口 / 退出）
const api = require('../../utils/api')

Page({
  data: {
    token: '',
    user: null,
    username: '',
    password: '',
    loading: false,
  },

  onShow() {
    if (this.getTabBar()) this.getTabBar().setData({ selected: 3 })
    this.setData({
      token: wx.getStorageSync('token') || '',
      user: JSON.parse(wx.getStorageSync('user') || 'null'),
    })
  },

  onUsername(e) {
    this.setData({ username: e.detail.value })
  },
  onPassword(e) {
    this.setData({ password: e.detail.value })
  },

  /** 登录 */
  login() {
    const { username, password } = this.data
    if (!username || !password) {
      wx.showToast({ title: '请输入账号和密码', icon: 'none' })
      return
    }
    this.setData({ loading: true })
    api
      .post('/auth/login', { username, password })
      .then((res) => {
        wx.setStorageSync('token', res.access_token)
        wx.setStorageSync('user', JSON.stringify(res.user))
        this.setData({ token: res.access_token, user: res.user })
        wx.showToast({ title: '登录成功', icon: 'success' })
      })
      .finally(() => this.setData({ loading: false }))
  },

  /** 查看订单 */
  goOrders() {
    wx.navigateTo({ url: '/pages/order/order' })
  },

  /** 地址管理 */
  goAddresses() {
    wx.navigateTo({ url: '/pages/address/address' })
  },

  /** 退出登录 */
  logout() {
    wx.removeStorageSync('token')
    wx.removeStorageSync('user')
    this.setData({ token: '', user: null })
  },
})

const api = require('../../utils/api')

Page({
  data: {
    orderId: '',
    orderNo: '',
    amount: '0.00',
    selectedMethod: 'wechat',
    paying: false,
    paymentMethods: [
      { value: 'wechat', icon: '💳', name: '微信支付', desc: '使用微信安全支付' },
      { value: 'cod', icon: '📦', name: '货到付款', desc: '收货时向配送员支付' },
    ],
  },

  onLoad(options) {
    this.setData({
      orderId: options.orderId || '',
      orderNo: options.orderNo || '',
      amount: Number(options.amount || 0).toFixed(2),
    })
  },

  selectMethod(e) {
    this.setData({ selectedMethod: e.currentTarget.dataset.value })
  },

  confirmPayment() {
    if (!this.data.orderId) {
      wx.showToast({ title: '订单信息无效', icon: 'none' })
      return
    }
    this.setData({ paying: true })
    api.put('/orders/' + this.data.orderId + '/status', { status: 1 })
      .then(() => {
        wx.showToast({ title: '支付成功', icon: 'success' })
        setTimeout(() => wx.switchTab({ url: '/pages/mine/mine' }), 800)
      })
      .finally(() => this.setData({ paying: false }))
  },
})

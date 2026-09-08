// pages/order/order.js 订单（列表 + 下单两种模式）
const api = require('../../utils/api')

Page({
  data: {
    mode: 'list',      // list=订单列表, create=下单
    source: '',        // 下单来源：cart=购物车, immediate=立即购买
    orders: [],
    status: null,
    statusTabs: [
      { label: '全部', value: null },
      { label: '待付款', value: 0 },
      { label: '待发货', value: 1 },
      { label: '待收货', value: 2 },
      { label: '已完成', value: 3 },
      { label: '已取消', value: 4 },
    ],
    orderItems: [],
    total: '0.00',
    addresses: [],
    selectedAddressId: null,
    useNewAddress: false,
    address: { name: '', phone: '', detail: '' },
    remark: '',
    submitting: false,
  },

  onLoad(options) {
    if (options.from === 'cart') {
      this.setData({ mode: 'create', source: 'cart' })
      this.buildCartItems()
    } else if (options.items) {
      this.setData({ mode: 'create', source: 'immediate' })
      this.buildImmediateItems(JSON.parse(decodeURIComponent(options.items)))
    }
  },

  onShow() {
    if (this.data.mode === 'list') this.loadOrders()
    else this.loadAddresses()
  },

  /** 加载预设地址 */
  loadAddresses() {
    api.get('/addresses').then((addresses) => {
      const selected = addresses.find((item) => item.is_default) || addresses[0]
      this.setData({
        addresses,
        selectedAddressId: selected ? selected.id : null,
        useNewAddress: !selected,
      })
    })
  },

  selectAddress(e) {
    this.setData({
      selectedAddressId: Number(e.currentTarget.dataset.id),
      useNewAddress: false,
    })
  },

  onUseNewAddress() {
    this.setData({
      useNewAddress: true,
      selectedAddressId: null,
      address: { name: '', phone: '', detail: '' },
    })
  },

  /** 加载我的订单 */
  loadOrders() {
    const params = { page: 1, size: 50 }
    if (this.data.status !== null) params.status = this.data.status
    api.get('/orders', params).then((res) => {
      const orders = (res.items || []).map((order) => ({
        ...order,
        items: (order.items || []).map((item) => ({
          ...item,
          product_image: api.fullUrl(item.product_image),
        })),
      }))
      this.setData({ orders })
    })
  },

  /** 取消待付款订单 */
  cancelOrder(e) {
    const orderId = e.currentTarget.dataset.id
    wx.showModal({
      title: '取消订单',
      content: '确定取消这个待付款订单吗？',
      confirmText: '确认取消',
      confirmColor: '#e4393c',
      success: (res) => {
        if (!res.confirm) return
        wx.showLoading({ title: '取消中' })
        api.put('/orders/' + orderId + '/status', { status: 4 })
          .then(() => {
            wx.hideLoading()
            wx.showToast({ title: '订单已取消', icon: 'success' })
            this.loadOrders()
          })
          .catch(() => wx.hideLoading())
      },
    })
  },

  /** 切换状态 */
  onStatusTap(e) {
    this.setData({ status: e.currentTarget.dataset.value })
    this.loadOrders()
  },

  /** 立即购买：按指定商品构建清单 */
  buildImmediateItems(items) {
    Promise.all(items.map((it) => api.get('/products/' + it.product_id))).then((products) => {
      const orderItems = products.map((p, i) => ({
        product_id: p.id,
        product_name: p.name,
        product_image: api.fullUrl(p.cover_image),
        price: Number(p.price),
        quantity: items[i].quantity,
      }))
      this.setItems(orderItems)
    })
  },

  /** 购物车结算：展示购物车全部商品 */
  buildCartItems() {
    api.get('/cart').then((res) => {
      const orderItems = res.map((i) => ({
        product_id: i.product_id,
        product_name: i.product_name,
        product_image: api.fullUrl(i.product_image),
        price: Number(i.price),
        quantity: i.quantity,
      }))
      this.setItems(orderItems)
    })
  },

  /** 设置清单并计算总价 */
  setItems(orderItems) {
    const total = orderItems.reduce((s, i) => s + i.price * i.quantity, 0)
    this.setData({ orderItems, total: total.toFixed(2) })
  },

  /** 收货信息输入 */
  onAddressInput(e) {
    const field = e.currentTarget.dataset.field
    this.setData({ [`address.${field}`]: e.detail.value })
  },

  onRemarkInput(e) {
    this.setData({ remark: e.detail.value })
  },

  /** 提交订单 */
  submitOrder() {
    const { address, addresses, selectedAddressId, useNewAddress, orderItems, remark, source } = this.data
    if (!orderItems.length) {
      wx.showToast({ title: '没有可结算的商品', icon: 'none' })
      return
    }
    if ((!useNewAddress && !selectedAddressId) || (useNewAddress && (!address.name || !address.phone || !address.detail))) {
      wx.showToast({ title: '请填写收货信息', icon: 'none' })
      return
    }
    this.setData({ submitting: true })

    const addressIdPromise = useNewAddress
      ? api.post('/addresses', {
        name: address.name,
        phone: address.phone,
        detail: address.detail,
        is_default: addresses.length ? 0 : 1,
      }).then((addr) => addr.id)
      : Promise.resolve(selectedAddressId)

    addressIdPromise
      .then((addressId) => {
        const payload = { address_id: addressId, remark }
        // 立即购买需显式传商品；购物车结算不传（后端读购物车并清空）
        if (source === 'immediate') {
          payload.items = orderItems.map((i) => ({
            product_id: i.product_id,
            quantity: i.quantity,
          }))
        }
        return api.post('/orders', payload)
      })
      .then((order) => {
        wx.showToast({ title: '下单成功', icon: 'success' })
        wx.navigateTo({
          url: '/pages/payment/payment?orderId=' + order.id +
            '&orderNo=' + encodeURIComponent(order.order_no) +
            '&amount=' + order.total_amount,
        })
      })
      .finally(() => this.setData({ submitting: false }))
  },
})

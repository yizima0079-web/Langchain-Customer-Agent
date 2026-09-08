Component({
  data: {
    selected: 0,
    list: [
      { pagePath: '/pages/index/index', text: '首页', icon: '⌂' },
      { pagePath: '/pages/chat/chat', text: '客服', icon: '✦' },
      { pagePath: '/pages/cart/cart', text: '购物车', icon: '🛒' },
      { pagePath: '/pages/mine/mine', text: '我的', icon: '♙' },
    ],
  },

  methods: {
    switchTab(e) {
      const index = Number(e.currentTarget.dataset.index)
      this.setData({ selected: index })
      wx.switchTab({ url: e.currentTarget.dataset.path })
    },
  },
})

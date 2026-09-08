// app.js 小程序全局入口
App({
  globalData: {
    // 后端服务地址（真机调试请改为电脑局域网 IP，如 http://192.168.x.x:8000）
    baseUrl: 'http://127.0.0.1:8000',
    token: '',
    userInfo: null,
  },
  onLaunch() {
    // 启动时读取本地缓存的登录态
    this.globalData.token = wx.getStorageSync('token') || ''
  },
})

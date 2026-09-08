const api = require('../../utils/api')

Page({
  data: {
    addresses: [],
    showForm: false,
    editingId: null,
    saving: false,
    form: { name: '', phone: '', region: '', detail: '', is_default: false },
  },

  onShow() {
    this.loadAddresses()
  },

  loadAddresses() {
    api.get('/addresses').then((addresses) => this.setData({ addresses }))
  },

  showAddForm() {
    this.setData({ showForm: true, editingId: null, form: { name: '', phone: '', region: '', detail: '', is_default: !this.data.addresses.length } })
  },

  editAddress(e) {
    const item = this.data.addresses.find((address) => address.id === Number(e.currentTarget.dataset.id))
    if (!item) return
    this.setData({
      showForm: true,
      editingId: item.id,
      form: {
        name: item.name,
        phone: item.phone,
        region: [item.province, item.city, item.district].filter(Boolean).join(''),
        detail: item.detail,
        is_default: !!item.is_default,
      },
    })
  },

  onInput(e) {
    this.setData({ [`form.${e.currentTarget.dataset.field}`]: e.detail.value })
  },

  onDefaultChange(e) {
    this.setData({ 'form.is_default': e.detail.value.includes('default') })
  },

  saveAddress() {
    const { form, editingId } = this.data
    if (!form.name || !form.phone || !form.detail) {
      wx.showToast({ title: '请填写完整地址', icon: 'none' })
      return
    }
    const data = { name: form.name, phone: form.phone, detail: form.detail, is_default: form.is_default ? 1 : 0 }
    if (form.region) data.detail = form.region + ' ' + form.detail
    this.setData({ saving: true })
    const request = editingId ? api.put('/addresses/' + editingId, data) : api.post('/addresses', data)
    request.then(() => {
      wx.showToast({ title: '保存成功', icon: 'success' })
      this.setData({ showForm: false })
      this.loadAddresses()
    }).finally(() => this.setData({ saving: false }))
  },

  cancelForm() { this.setData({ showForm: false }) },

  setDefault(e) {
    api.put('/addresses/' + e.currentTarget.dataset.id, { is_default: 1 }).then(() => this.loadAddresses())
  },

  deleteAddress(e) {
    const id = e.currentTarget.dataset.id
    wx.showModal({ title: '删除地址', content: '确定删除这个地址吗？', success: (res) => {
      if (res.confirm) api.del('/addresses/' + id).then(() => this.loadAddresses())
    } })
  },
})

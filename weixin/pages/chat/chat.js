// pages/chat/chat.js AI 智能客服（RAG 增强检索）
const api = require('../../utils/api')

Page({
  data: {
    messages: [],
    input: '',
    sending: false,
    sessionId: null,
    scrollIntoView: '',
  },

  onShow() {
    if (this.getTabBar()) this.getTabBar().setData({ selected: 1 })
  },

  onInput(e) {
    this.setData({ input: e.detail.value })
  },

  /** 发送消息 */
  send() {
    const text = this.data.input.trim()
    if (!text || this.data.sending) return

    // 追加用户消息
    let messages = this.data.messages.concat([{ role: 'user', content: text }])
    this.setData({
      messages,
      input: '',
      sending: true,
      scrollIntoView: 'msg-' + (messages.length - 1),
    })

    const assistantIndex = messages.length
    messages.push({ role: 'assistant', content: '', streaming: true })
    this.setData({ messages, scrollIntoView: 'msg-' + assistantIndex })

    api.streamChat(
      { session_id: this.data.sessionId, message: text },
      (event) => {
        if (event.type === 'meta') {
          this.setData({ sessionId: event.session_id })
        } else if (event.type === 'delta') {
          const next = this.data.messages.slice()
          next[assistantIndex].content += event.content || ''
          this.setData({ messages: next, scrollIntoView: 'msg-' + assistantIndex })
        } else if (event.type === 'error') {
          const next = this.data.messages.slice()
          next[assistantIndex].content = event.message
          this.setData({ messages: next })
        }
      },
    ).catch(() => {
      const next = this.data.messages.slice()
      if (next[assistantIndex]) next[assistantIndex].content = '抱歉，客服连接失败，请稍后重试。'
      this.setData({ messages: next })
    }).finally(() => {
      const next = this.data.messages.slice()
      if (next[assistantIndex]) next[assistantIndex].streaming = false
      this.setData({ messages: next, sending: false })
    })
  },
})

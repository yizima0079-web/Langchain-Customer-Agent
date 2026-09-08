<template>
  <div class="chat-page">
    <el-card class="chat-card">
      <template #header><div class="chat-header"><div><strong>AI 智能客服</strong><span>知识库问答工作台</span></div><el-tag type="success" effect="light" size="small">服务在线</el-tag></div></template>

      <!-- 消息列表 -->
      <div ref="msgRef" class="messages">
        <div v-for="(m, i) in messages" :key="i" :class="['msg', m.role]">
          <div class="msg-avatar">{{ m.role === 'assistant' ? 'AI' : '我' }}</div>
          <div class="bubble">{{ m.content }}</div>
        </div>
        <div v-if="!messages.length" class="empty">向 AI 客服提问，回答基于知识库 RAG 检索生成</div>
      </div>

      <!-- 输入栏 -->
      <div class="input-bar">
        <el-input
          v-model="input"
          placeholder="输入问题，例如：如何申请退货？"
          @keyup.enter="send"
        />
        <el-button type="primary" :loading="sending" @click="send">发送</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { nextTick, ref } from 'vue'
import { chat } from '@/api'

const messages = ref([])
const input = ref('')
const sending = ref(false)
const sessionId = ref(null)
const msgRef = ref(null)

/** 发送消息并接收 AI 回复 */
async function send() {
  const text = input.value.trim()
  if (!text || sending.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  sending.value = true
  try {
    const data = await chat({ session_id: sessionId.value, message: text })
    sessionId.value = data.session_id
    messages.value.push({ role: 'assistant', content: data.answer, sources: data.sources })
  } finally {
    sending.value = false
  }
  scrollToBottom()
}

/** 滚动到底部 */
function scrollToBottom() {
  nextTick(() => {
    if (msgRef.value) msgRef.value.scrollTop = msgRef.value.scrollHeight
  })
}
</script>

<style scoped>
.chat-page {
  height: calc(100vh - 130px);
}
.chat-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.chat-header { display: flex; align-items: center; justify-content: space-between; }
.chat-header strong { display: block; color: #1b2a48; font-size: 15px; }
.chat-header span { display: block; margin-top: 4px; color: #9aa6b8; font-size: 11px; font-weight: 400; }
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: linear-gradient(135deg, #f8faff, #f4f7fb);
  border: 1px solid #edf1f7;
  border-radius: 10px;
  min-height: 360px;
}
.msg {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 9px;
}
.msg.user {
  justify-content: flex-end;
  flex-direction: row-reverse;
}
.msg-avatar { display: grid; flex: 0 0 28px; place-items: center; width: 28px; height: 28px; border-radius: 9px; color: #fff; font-size: 10px; font-weight: 700; background: linear-gradient(135deg, #5f8ff3, #315dc3); }
.msg.user .msg-avatar { background: #dfe8f8; color: #52698f; }
.bubble {
  max-width: 70%;
  padding: 10px 14px;
  border: 1px solid #e9eef6;
  border-radius: 4px 12px 12px 12px;
  background: #fff;
  line-height: 1.6;
  word-break: break-all;
}
.msg.user .bubble {
  background: #409eff;
  color: #fff;
  border: 0;
  border-radius: 12px 4px 12px 12px;
}
.empty {
  text-align: center;
  color: #c0c4cc;
  padding-top: 60px;
}
.input-bar {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}
</style>

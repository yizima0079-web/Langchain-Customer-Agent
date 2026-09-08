<template>
  <div class="login-container">
    <div class="login-orbit orbit-one"></div><div class="login-orbit orbit-two"></div>
    <div class="login-shell">
      <section class="login-visual">
        <div class="brand-mark">AI</div>
        <div class="eyebrow">SMART COMMERCE OS</div>
        <h1>让每一次服务<br /><em>都更聪明</em></h1>
        <p>商品、订单、知识库与智能客服，集中在一个清晰高效的工作台。</p>
        <div class="visual-stat"><span class="pulse"></span><span>AI 服务系统在线</span><strong>24 / 7</strong></div>
      </section>
      <section class="login-card">
        <div class="welcome">欢迎回来<span>·</span></div>
        <div class="login-subtitle">登录管理后台，继续处理业务</div>
        <el-form :model="form" @keyup.enter="handleLogin">
          <el-form-item><el-input v-model="form.username" placeholder="管理员账号" :prefix-icon="User" size="large" /></el-form-item>
          <el-form-item><el-input v-model="form.password" type="password" placeholder="登录密码" :prefix-icon="Lock" size="large" show-password /></el-form-item>
          <el-button type="primary" size="large" class="login-btn" :loading="loading" @click="handleLogin">进入工作台</el-button>
        </el-form>
        <p class="tip">默认账号：admin <span>/</span> 123456</p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Lock, User } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({ username: 'admin', password: '123456' })
const loading = ref(false)

/** 登录：调用 store 并跳转后台首页 */
async function handleLogin() {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入账号和密码')
    return
  }
  loading.value = true
  try {
    await userStore.login(form)
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  position: relative;
  overflow: hidden;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at 12% 20%, #345fc6 0, transparent 28%), linear-gradient(135deg, #0c1937, #172f68 58%, #101b3b);
}
.login-container::before { content: ''; position: absolute; inset: 0; opacity: .13; background-image: linear-gradient(rgba(255,255,255,.18) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.18) 1px, transparent 1px); background-size: 42px 42px; mask-image: linear-gradient(to bottom right, #000, transparent 72%); }
.login-orbit { position: absolute; border: 1px solid rgba(164, 198, 255, .18); border-radius: 50%; }
.orbit-one { width: 520px; height: 520px; right: -180px; top: -160px; box-shadow: 0 0 0 36px rgba(99, 155, 255, .035), 0 0 0 72px rgba(99, 155, 255, .025); }
.orbit-two { width: 320px; height: 320px; left: -160px; bottom: -150px; }
.login-shell { position: relative; z-index: 1; display: grid; grid-template-columns: 1.05fr .95fr; width: min(850px, calc(100% - 40px)); min-height: 490px; overflow: hidden; border: 1px solid rgba(255,255,255,.2); border-radius: 24px; background: rgba(255,255,255,.96); box-shadow: 0 30px 90px rgba(4, 15, 48, .35); }
.login-visual { position: relative; padding: 54px 48px; color: #fff; background: linear-gradient(145deg, rgba(32, 78, 173, .98), rgba(22, 40, 97, .98)); }
.login-visual::after { content: ''; position: absolute; width: 230px; height: 230px; right: -80px; bottom: -75px; border: 32px solid rgba(127, 180, 255, .12); border-radius: 50%; }
.brand-mark { display: grid; place-items: center; width: 46px; height: 46px; margin-bottom: 42px; border: 1px solid rgba(255,255,255,.45); border-radius: 14px; color: #cfe1ff; font-weight: 800; letter-spacing: -1px; background: rgba(255,255,255,.12); }
.eyebrow { color: #b8d1ff; font-size: 11px; letter-spacing: 2.5px; }
.login-visual h1 { margin: 18px 0; font-size: 38px; line-height: 1.28; letter-spacing: -1px; }
.login-visual h1 em { color: #9bc4ff; font-style: normal; }
.login-visual p { max-width: 300px; color: #ccdcff; line-height: 1.8; }
.visual-stat { position: absolute; right: 48px; bottom: 46px; display: flex; align-items: center; gap: 8px; color: #cfe1ff; font-size: 12px; }
.visual-stat strong { margin-left: 8px; color: #fff; font-size: 13px; }
.pulse { width: 7px; height: 7px; border-radius: 50%; background: #58e0ad; box-shadow: 0 0 0 5px rgba(88,224,173,.14), 0 0 12px #58e0ad; }
.login-card {
  align-self: center;
  width: auto;
  padding: 54px 48px;
  border: 0;
  box-shadow: none;
}
.welcome { color: #17233c; font-size: 28px; font-weight: 700; }
.welcome span { color: #2f6df6; }
.login-subtitle { margin: 10px 0 30px; color: #8a96aa; font-size: 13px; }
.login-card :deep(.el-form-item) { margin-bottom: 18px; }
.login-card :deep(.el-input__wrapper) { border-radius: 10px; box-shadow: 0 0 0 1px #e6ebf3 inset; }
.login-card :deep(.el-input__wrapper.is-focus) { box-shadow: 0 0 0 1px #2f6df6 inset, 0 5px 15px rgba(47,109,246,.1); }
.login-btn {
  width: 100%;
  margin-top: 8px;
  border-radius: 10px;
  box-shadow: 0 8px 18px rgba(47,109,246,.23);
}
.tip {
  margin-top: 22px;
  text-align: center;
  color: #9aa5b7;
  font-size: 12px;
}
.tip span { padding: 0 5px; color: #c3cad6; }
@media (max-width: 700px) { .login-visual { display: none; } .login-shell { display: block; min-height: auto; } .login-card { padding: 42px 32px; } }
</style>

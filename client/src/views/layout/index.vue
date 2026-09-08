<template>
  <el-container class="layout">
    <!-- 侧边栏 -->
    <el-aside width="228px" class="aside">
      <div class="logo"><span class="logo-mark">AI</span><span><b>智能客服</b><small>COMMERCE CONSOLE</small></span></div>
      <el-menu
        :default-active="$route.path"
        router
        background-color="#001529"
        text-color="#a6adb4"
        active-text-color="#ffffff"
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataAnalysis /></el-icon><span>数据统计</span>
        </el-menu-item>
        <el-menu-item index="/category">
          <el-icon><CollectionTag /></el-icon><span>分类管理</span>
        </el-menu-item>
        <el-menu-item index="/product">
          <el-icon><Goods /></el-icon><span>商品管理</span>
        </el-menu-item>
        <el-menu-item index="/banner">
          <el-icon><Picture /></el-icon><span>轮播图管理</span>
        </el-menu-item>
        <el-menu-item index="/order">
          <el-icon><Sell /></el-icon><span>订单管理</span>
        </el-menu-item>
        <el-menu-item index="/user">
          <el-icon><User /></el-icon><span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/knowledge">
          <el-icon><FolderOpened /></el-icon><span>知识库管理</span>
        </el-menu-item>
        <el-menu-item index="/chat">
          <el-icon><ChatDotRound /></el-icon><span>AI 客服调试</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <!-- 顶栏 -->
      <el-header class="header">
        <div class="header-context"><span class="context-dot"></span><span class="page-title">{{ $route.meta.title }}</span><span class="context-line">/ 管理工作台</span></div>
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <span class="avatar">{{ (userStore.user?.nickname || '管')[0] }}</span><span>{{ userStore.user?.nickname || '管理员' }}</span>
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>

      <!-- 内容区 -->
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

/** 顶栏下拉命令处理 */
async function handleCommand(command) {
  if (command === 'logout') {
    await ElMessageBox.confirm('确认退出登录？', '提示', { type: 'warning' })
    userStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.layout {
  height: 100%;
}
.aside {
  background: linear-gradient(180deg, #0b1836, #101f45);
  box-shadow: 8px 0 28px rgba(23, 52, 107, .1);
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 0 22px;
  color: #fff;
}
.logo-mark { display: grid; place-items: center; width: 32px; height: 32px; border: 1px solid rgba(160, 200, 255, .55); border-radius: 10px; color: #cce0ff; font-size: 12px; font-weight: 800; background: rgba(100, 157, 255, .18); }
.logo b { display: block; font-size: 15px; letter-spacing: 1px; }
.logo small { display: block; margin-top: 3px; color: #7186b0; font-size: 8px; letter-spacing: 1.2px; }
.aside :deep(.el-menu) { padding: 12px 10px; background: transparent; }
.aside :deep(.el-menu-item) { height: 46px; margin: 4px 0; border-radius: 10px; color: #9baac8; }
.aside :deep(.el-menu-item:hover) { color: #fff; background: rgba(94, 143, 235, .12); }
.aside :deep(.el-menu-item.is-active) { color: #fff; background: linear-gradient(90deg, rgba(69, 125, 236, .9), rgba(65, 112, 216, .42)); box-shadow: 0 8px 18px rgba(30, 86, 190, .2); }
.aside :deep(.el-menu-item .el-icon) { margin-right: 12px; font-size: 17px; }
.header {
  background: #fff;
  border-bottom: 1px solid #e8edf5;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.header-context { display: flex; align-items: center; gap: 10px; }
.context-dot { width: 7px; height: 7px; border-radius: 50%; background: #3ed09a; box-shadow: 0 0 0 4px rgba(62,208,154,.12); }
.page-title {
  font-size: 15px;
  font-weight: 600;
}
.context-line { color: #b1bac9; font-size: 12px; }
.user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  color: #394761;
  font-size: 13px;
}
.avatar { display: grid; place-items: center; width: 28px; height: 28px; border-radius: 50%; color: #fff; font-size: 12px; background: linear-gradient(135deg, #5d8ff7, #315ac0); }
.main {
  overflow: auto;
  background: #f4f7fb;
}
</style>

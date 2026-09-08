import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'

// Vite 配置：路径别名 + 开发代理（转发到后端 FastAPI）
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      // 后端 API 前缀
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      // 上传文件静态资源
      '/uploads14': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})

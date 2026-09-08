<template>
  <div class="page-container">
    <el-card>
      <!-- 上传区 -->
      <div class="filter-bar">
        <el-upload
          :show-file-list="false"
          :http-request="handleUpload"
          accept=".txt,.doc,.docx,.pdf,.md,.markdown"
        >
          <el-button type="primary" :icon="Upload">上传知识库文件</el-button>
        </el-upload>
        <span class="hint">支持 txt / doc / docx / pdf / markdown 格式，上传后自动解析并向量化</span>
      </div>

      <el-table :data="list" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="filename" label="文件名" min-width="200" />
        <el-table-column prop="file_type" label="类型" width="100" />
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="STATUS_TAG[row.status]">{{ STATUS_MAP[row.status] }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="chunk_count" label="文本块数" width="100" />
        <el-table-column prop="error_msg" label="失败原因" min-width="180" show-overflow-tooltip />
        <el-table-column prop="created_at" label="上传时间" width="170" />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'
import { deleteKnowledge, getKnowledge, uploadKnowledge } from '@/api'

const STATUS_MAP = { 0: '待处理', 1: '已向量化', 2: '处理失败' }
const STATUS_TAG = { 0: 'warning', 1: 'success', 2: 'danger' }

const list = ref([])
const loading = ref(false)

/** 加载知识库文件列表 */
async function loadData() {
  loading.value = true
  try {
    list.value = await getKnowledge()
  } finally {
    loading.value = false
  }
}

/** 上传并向量化 */
async function handleUpload(options) {
  await uploadKnowledge(options.file)
  ElMessage.success('上传成功，正在解析向量化')
  loadData()
}

/** 删除知识库文件 */
async function handleDelete(row) {
  await ElMessageBox.confirm(`确认删除文件「${row.filename}」？`, '提示', { type: 'warning' })
  await deleteKnowledge(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>

<style scoped>
.hint {
  color: #909399;
  font-size: 12px;
}
</style>

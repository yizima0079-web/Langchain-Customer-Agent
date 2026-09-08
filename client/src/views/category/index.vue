<template>
  <div class="page-container">
    <div class="page-intro">
      <div><div class="eyebrow">CATALOG STRUCTURE</div><h2>分类管理</h2><p>维护商品目录，让用户更快找到需要的商品。</p></div>
      <div class="intro-metric"><strong>{{ list.length }}</strong><span>个分类</span></div>
    </div>
    <el-card class="data-card" shadow="never">
      <div class="table-toolbar">
        <span class="toolbar-title">全部分类</span><span class="toolbar-hint">共 {{ list.length }} 项</span>
        <el-button type="primary" :icon="Plus" @click="openDialog()">新增分类</el-button>
      </div>

      <el-table :data="list" stripe size="small" row-class-name="compact-row">
        <el-table-column prop="id" label="ID" width="76" />
        <el-table-column prop="name" label="分类名称" width="220" show-overflow-tooltip />
        <el-table-column prop="sort" label="排序" width="100" />
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑分类' : '新增分类'" width="420px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="分类名称">
          <el-input v-model="form.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort" :min="0" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" :active-value="1" :inactive-value="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { createCategory, deleteCategory, getCategories, updateCategory } from '@/api'

const list = ref([])
const dialogVisible = ref(false)
const form = reactive({ id: null, name: '', sort: 0, status: 1 })

/** 加载分类列表 */
async function loadData() {
  list.value = await getCategories()
}

/** 打开新增/编辑弹窗 */
function openDialog(row) {
  if (row) {
    Object.assign(form, { id: row.id, name: row.name, sort: row.sort, status: row.status })
  } else {
    Object.assign(form, { id: null, name: '', sort: 0, status: 1 })
  }
  dialogVisible.value = true
}

/** 保存分类 */
async function handleSave() {
  if (!form.name) {
    ElMessage.warning('请输入分类名称')
    return
  }
  const payload = { name: form.name, sort: form.sort, status: form.status }
  if (form.id) {
    await updateCategory(form.id, payload)
  } else {
    await createCategory(payload)
  }
  ElMessage.success('保存成功')
  dialogVisible.value = false
  loadData()
}

/** 删除分类 */
async function handleDelete(row) {
  await ElMessageBox.confirm(`确认删除分类「${row.name}」？`, '提示', { type: 'warning' })
  await deleteCategory(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>

<style scoped>
.page-intro { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 18px; }
.eyebrow { margin-bottom: 7px; color: #6c91df; font-size: 10px; font-weight: 700; letter-spacing: 2px; }
h2 { color: #17233c; font-size: 24px; letter-spacing: -.5px; }
.page-intro p { margin-top: 7px; color: #8a96aa; font-size: 13px; }
.intro-metric { display: flex; align-items: baseline; gap: 7px; padding: 11px 17px; border: 1px solid #e5ebf5; border-radius: 12px; background: #fff; }
.intro-metric strong { color: #2f6df6; font-size: 24px; }
.intro-metric span { color: #8b97aa; font-size: 12px; }
.data-card { overflow: hidden; }
.table-toolbar { display: flex; align-items: center; gap: 10px; margin-bottom: 13px; }
.toolbar-title { color: #243451; font-size: 15px; font-weight: 650; }
.toolbar-hint { flex: 1; color: #9aa6b8; font-size: 12px; }
.data-card :deep(.el-table .cell) { padding-top: 2px; padding-bottom: 2px; }
.data-card :deep(.el-table__row) { height: 48px; }
</style>

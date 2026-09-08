<template>
  <div class="page-container">
    <el-card>
      <div class="filter-bar">
        <el-button type="primary" :icon="Plus" @click="openDialog()">新增轮播图</el-button>
      </div>

      <el-table :data="list" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="标题" min-width="160" />
        <el-table-column label="图片" width="160">
          <template #default="{ row }">
            <el-image
              :src="row.image"
              :preview-src-list="[row.image]"
              preview-teleported
              fit="cover"
              style="width: 110px; height: 44px; border-radius: 4px"
            />
          </template>
        </el-table-column>
        <el-table-column prop="sort" label="排序" width="90" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="170" />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑轮播图' : '新增轮播图'" width="480px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="请输入轮播标题（可为空）" />
        </el-form-item>
        <el-form-item label="图片">
          <el-upload
            :show-file-list="false"
            :http-request="handleUpload"
            accept=".jpg,.jpeg,.png,.gif,.webp"
          >
            <el-button :icon="Upload">上传图片</el-button>
          </el-upload>
          <img v-if="form.image" :src="form.image" class="preview-img" alt="预览" />
          <div v-else class="preview-empty">建议尺寸 750×300，未上传</div>
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
        <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Upload } from '@element-plus/icons-vue'
import { createBanner, deleteBanner, getBanners, updateBanner, uploadImage } from '@/api'

const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const saving = ref(false)
const form = reactive({ id: null, title: '', image: '', sort: 0, status: 1 })

/** 加载轮播图列表 */
async function loadData() {
  loading.value = true
  try {
    list.value = await getBanners(false)
  } finally {
    loading.value = false
  }
}

/** 打开新增/编辑弹窗 */
function openDialog(row) {
  if (row) {
    Object.assign(form, { id: row.id, title: row.title, image: row.image, sort: row.sort, status: row.status })
  } else {
    Object.assign(form, { id: null, title: '', image: '', sort: 0, status: 1 })
  }
  dialogVisible.value = true
}

/** 上传图片到 /uploads14/banner/，成功后回填 URL */
async function handleUpload(options) {
  const { url } = await uploadImage(options.file, 'banner')
  form.image = url
  ElMessage.success('图片上传成功')
}

/** 保存轮播图 */
async function handleSave() {
  if (!form.image) {
    ElMessage.warning('请先上传图片')
    return
  }
  saving.value = true
  try {
    const payload = { title: form.title, image: form.image, sort: form.sort, status: form.status }
    if (form.id) {
      await updateBanner(form.id, payload)
    } else {
      await createBanner(payload)
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    loadData()
  } finally {
    saving.value = false
  }
}

/** 删除轮播图 */
async function handleDelete(row) {
  await ElMessageBox.confirm(`确认删除轮播图「${row.title || row.id}」？`, '提示', { type: 'warning' })
  await deleteBanner(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>

<style scoped>
.preview-img {
  display: block;
  margin-top: 10px;
  width: 240px;
  height: 96px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #e6e6e6;
}
.preview-empty {
  margin-top: 10px;
  font-size: 12px;
  color: #909399;
}
</style>

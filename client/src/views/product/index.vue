<template>
  <div class="page-container">
    <el-card>
      <!-- 筛选栏 -->
      <div class="filter-bar">
        <el-input
          v-model="query.keyword"
          placeholder="商品名称"
          clearable
          style="width: 200px"
          @keyup.enter="handleSearch"
        />
        <el-select v-model="query.category_id" placeholder="全部分类" clearable style="width: 160px">
          <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
        <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
        <el-button type="success" :icon="Plus" @click="openDialog()">新增商品</el-button>
      </div>

      <el-table :data="list" border stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column label="封面" width="80">
          <template #default="{ row }">
            <el-image
              v-if="row.cover_image"
              :src="row.cover_image"
              style="width: 50px; height: 50px"
              fit="cover"
            />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" min-width="140" />
        <el-table-column prop="category_name" label="分类" width="100" />
        <el-table-column prop="price" label="售价" width="100" />
        <el-table-column prop="stock" label="库存" width="80" />
        <el-table-column prop="sales" label="销量" width="80" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '上架' : '下架' }}
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

      <!-- 分页 -->
      <div class="pagination-wrap">
        <el-pagination
          v-model:current-page="query.page"
          v-model:page-size="query.size"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="loadData"
        />
      </div>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑商品' : '新增商品'" width="640px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="商品名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category_id" placeholder="请选择分类" style="width: 100%">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="售价">
          <el-input-number v-model="form.price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="原价">
          <el-input-number v-model="form.original_price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="库存">
          <el-input-number v-model="form.stock" :min="0" />
        </el-form-item>
        <el-form-item label="封面图">
          <el-upload
            :show-file-list="false"
            :http-request="handleUpload"
            accept="image/*"
          >
            <el-image v-if="form.cover_image" :src="form.cover_image" style="width: 120px; height: 120px" fit="cover" />
            <el-button v-else :icon="Plus">上传图片</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="商品描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
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
import { Plus, Search } from '@element-plus/icons-vue'
import {
  createProduct,
  deleteProduct,
  getCategories,
  getProducts,
  updateProduct,
  uploadImage,
} from '@/api'

const list = ref([])
const total = ref(0)
const categories = ref([])
const dialogVisible = ref(false)

const query = reactive({ page: 1, size: 10, keyword: '', category_id: null })
const form = reactive({
  id: null,
  category_id: null,
  name: '',
  description: '',
  price: 0,
  original_price: null,
  stock: 0,
  cover_image: '',
  status: 1,
})

/** 加载商品列表 */
async function loadData() {
  const params = { page: query.page, size: query.size }
  if (query.keyword) params.keyword = query.keyword
  if (query.category_id) params.category_id = query.category_id
  const data = await getProducts(params)
  list.value = data.items
  total.value = data.total
}

/** 查询 */
function handleSearch() {
  query.page = 1
  loadData()
}

/** 加载分类下拉 */
async function loadCategories() {
  categories.value = await getCategories()
}

/** 上传封面图 */
async function handleUpload(options) {
  const data = await uploadImage(options.file, 'product')
  form.cover_image = data.url
  ElMessage.success('上传成功')
}

/** 打开新增/编辑弹窗 */
function openDialog(row) {
  if (row) {
    Object.assign(form, {
      id: row.id,
      category_id: row.category_id,
      name: row.name,
      description: row.description,
      price: Number(row.price),
      original_price: row.original_price != null ? Number(row.original_price) : null,
      stock: row.stock,
      cover_image: row.cover_image,
      status: row.status,
    })
  } else {
    Object.assign(form, {
      id: null, category_id: null, name: '', description: '', price: 0,
      original_price: null, stock: 0, cover_image: '', status: 1,
    })
  }
  dialogVisible.value = true
}

/** 保存商品 */
async function handleSave() {
  if (!form.name || !form.category_id) {
    ElMessage.warning('请填写商品名称并选择分类')
    return
  }
  const payload = { ...form }
  delete payload.id
  if (form.id) {
    await updateProduct(form.id, payload)
  } else {
    await createProduct(payload)
  }
  ElMessage.success('保存成功')
  dialogVisible.value = false
  loadData()
}

/** 删除商品 */
async function handleDelete(row) {
  await ElMessageBox.confirm(`确认删除商品「${row.name}」？`, '提示', { type: 'warning' })
  await deleteProduct(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(() => {
  loadData()
  loadCategories()
})
</script>

<template>
  <div class="page-container">
    <el-card>
      <!-- 筛选栏 -->
      <div class="filter-bar">
        <el-select v-model="query.status" placeholder="全部状态" clearable style="width: 160px">
          <el-option v-for="(v, k) in STATUS_MAP" :key="k" :label="v" :value="Number(k)" />
        </el-select>
        <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
      </div>

      <el-table :data="list" border stripe>
        <el-table-column prop="order_no" label="订单号" width="180" />
        <el-table-column prop="user_id" label="用户ID" width="90" />
        <el-table-column prop="total_amount" label="金额" width="110" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="STATUS_TAG[row.status]">{{ STATUS_MAP[row.status] }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="下单时间" width="170" />
        <el-table-column label="商品明细" min-width="220">
          <template #default="{ row }">
            <div v-for="item in row.items" :key="item.id" class="item-line">
              {{ item.product_name }} × {{ item.quantity }}
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.status === 1" size="small" type="primary" @click="changeStatus(row, 2)">发货</el-button>
            <el-button v-if="row.status === 2" size="small" type="success" @click="changeStatus(row, 3)">完成</el-button>
          </template>
        </el-table-column>
      </el-table>

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
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getOrders, updateOrderStatus } from '@/api'

const STATUS_MAP = { 0: '待付款', 1: '待发货', 2: '待收货', 3: '已完成', 4: '已取消' }
const STATUS_TAG = { 0: 'warning', 1: 'primary', 2: 'info', 3: 'success', 4: 'danger' }

const list = ref([])
const total = ref(0)
const query = reactive({ page: 1, size: 10, status: null })

/** 加载订单列表 */
async function loadData() {
  const params = { page: query.page, size: query.size }
  if (query.status !== null) params.status = query.status
  const data = await getOrders(params)
  list.value = data.items
  total.value = data.total
}

/** 查询 */
function handleSearch() {
  query.page = 1
  loadData()
}

/** 修改订单状态 */
async function changeStatus(row, status) {
  await updateOrderStatus(row.id, status)
  ElMessage.success('操作成功')
  loadData()
}

onMounted(loadData)
</script>

<style scoped>
.item-line {
  font-size: 12px;
  color: #606266;
  line-height: 20px;
}
</style>

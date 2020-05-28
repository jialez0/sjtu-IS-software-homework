<template>
  <div class="app-container">
    <el-input v-model="filterText" placeholder="Filter keyword" style="margin-bottom:30px;" />
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="场所ID" width="200">
        <template slot-scope="scope">
          {{ scope.row.locationid }}
        </template>
      </el-table-column>
      <el-table-column label="场所">
        <template slot-scope="scope">
          {{ scope.row.locationName }}
        </template>
      </el-table-column>
      <el-table-column label="入场人数" width="200" align="center">
        <template slot-scope="scope">
          {{ scope.row.enterNumber }}
        </template>
      </el-table-column>
      <el-table-column label="警戒人数" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.alertNumber }}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="状态" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getLocationList } from '@/api/table'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        正常: 'success',
        关闭: 'gray',
        警戒: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      filterText: '',
      list: null,
      listLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getLocationList().then(response => {
        this.list = response.data.items
        this.listLoading = false
      })
    }
  }
}
</script>

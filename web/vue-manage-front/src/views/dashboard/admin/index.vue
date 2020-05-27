<template>
  <div class="dashboard-editor-container">

    <panel-group :panel-data="panelData" @handleSetLineChartData="handleSetLineChartData" />

    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <component :is="chosenChart" :chart-data="chartData" />
    </el-row>
  </div>
</template>

<script>
import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'
import PieChart from './components/PieChart'
import BarChart from './components/BarChart'
import { getCharts } from '@/api/charts.js'

export default {
  name: 'DashboardAdmin',
  components: {
    PanelGroup,
    LineChart,
    PieChart,
    BarChart
  },
  data() {
    return {
      lineChartData: {},
      panelData: {},
      pieChartData: {},
      chosenChart: 'LineChart',
      chartData: {}
    }
  },
  created() {
    this.fetchChartsData()
  },
  methods: {
    handleSetLineChartData(type) {
      if (type === 'locations') {
        this.chosenChart = 'PieChart'
        this.chartData = this.pieChartData
      } else {
        this.chosenChart = 'LineChart'
        this.chartData = this.lineChartData
      }
    },
    fetchChartsData() {
      getCharts().then(response => {
        this.lineChartData = response.data.line
        this.panelData = response.data.panel
        this.pieChartData = response.data.pie
        this.handleSetLineChartData('locations')
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>

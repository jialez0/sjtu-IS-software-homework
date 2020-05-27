<template>
  <div class="dashboard-editor-container">

    <panel-group @handleSetLineChartData="handleSetLineChartData" :panel-data="panelData" />

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
import getCharts from '@/api/charts.js'

const lineChartData = {
  newVisitis: {
    expectedData: [100, 120, 161, 134, 105, 160],
    actualData: [120, 82, 91, 154, 162, 140]
  },
  messages: {
    expectedData: [200, 192, 120, 144, 160, 130, 140],
    actualData: [180, 160, 151, 106, 145, 150, 130]
  },
  purchases: {
    expectedData: [80, 100, 121, 104, 105, 90, 100],
    actualData: [120, 90, 100, 138, 142, 130, 130]
  },
  shoppings: {
    expectedData: [130, 140, 141, 142, 145, 150, 160],
    actualData: [120, 82, 91, 154, 162, 140, 130]
  }
}

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
      lineChartData: {
        expectedData: [100, 120, 161, 134, 105, 160],
        actualData: [120, 82, 91, 154, 162, 140]
      },
      panelData: {
        new: 10000,
        all: 81222,
        location: 14562
      }, 
      chartData: lineChartData.newVisitis,
      chosenChart: 'LineChart'
    }
  },
  methods: {
    handleSetLineChartData(type) {
      if (type === 'location') {
        this.chosenChart = 'PieChart'
        this.chartData = this.pieChartData
      }
      else {
        this.chosenChart = 'LineChart'
        this.chartData = this.lineChartData
        // this.chartData = lineChartData[type];
      }
    },
    fetchChartsData() {
      getCharts().then(response => {
        this.lineChartData = response.data.line
        this.panelData = response.data.panel
        this.pieChartData = response.data.pie
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

import request from '@/utils/request'

export function getCharts(params) {
  return request({
    url: '/vue-admin-template/charts',
    method: 'get',
    params
  })
}

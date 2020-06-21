import request from '@/utils/request'

export function getCharts(params) {
  return request({
    url: '/charts',
    method: 'get',
    params
  })
}

import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/table/userlist',
    method: 'get',
    params
  })
}

export function getLocationList(params) {
  return request({
    url: '/table/locationlist',
    method: 'get',
    params
  })
}

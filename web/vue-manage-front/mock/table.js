import Mock from 'mockjs'

const data = Mock.mock({
  'items|30': [{
    id: '@id',
    nickName: '@string',
    'status|1': ['正常', '过期', '离校'],
    'age|0-100': 0,
    phoneNumber: '@integer(13333333333, 17777777777)',
    stopTime: '@datetime',
    startTime: '@datetime'
  }]
})

const data2 = Mock.mock({
  'items|30': [{
    locationid: '@id',
    locationName: '@string',
    'status|1': ['正常', '警戒', '关闭'],
    'enterNumber|0-1000': 0,
    'alertNumber|500-2000': 0
  }]
})

export default [
  {
    url: '/table/userlist',
    type: 'get',
    response: config => {
      const items = data.items
      return {
        code: 20000,
        data: {
          total: items.length,
          items: items
        }
      }
    }
  },
  {
    url: '/table/locationlist',
    type: 'get',
    response: config => {
      const items = data2.items
      return {
        code: 20000,
        data: {
          total: items.length,
          items: items
        }
      }
    }
  }
]

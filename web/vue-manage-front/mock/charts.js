
export default [
  {
    url: '/charts',
    type: 'get',
    response: () => {
      return {
        code: 20000,
        data: {
          line: {
            dates: ['5/21', '5/22', '5/23', '5/24', '5/25', '5/26', '5/27'],
            // dates: ['一餐', '二餐', '三餐', '四餐', '玉兰苑', '新图', '电院'],
            newVisits: [0, 123, 120, 82, 91, 154, 162],
            allVisits: [180, 160, 151, 106, 145, 150, 130]
          },
          panel: {
            new: 10032,
            all: 81222,
            location: 14562
          },
          pie: {
            locationName: ['一餐', '二餐', '三餐', '四餐', '玉兰苑', '新图', '电院'],
            peopleNum: [123, 522, 224, 490, 111, 99, 10]
          }
        }
      }
    }
  }
]

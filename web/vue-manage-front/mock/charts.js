export default [
  {
    url: "/charts",
    type: "get",
    response: () => {
      return {
        code: 20000,
        data: {
          line: {
            dates: ["6/14", "6/15", "6/16", "6/17", "6/18", "6/19", "6/20"],
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
            locationName: [
              "一餐",
              "二餐",
              "三餐",
              "四餐",
              "玉兰苑",
              "新图",
              "电院"
            ],
            peopleNum: [123, 522, 224, 490, 111, 99, 10]
          }
        }
      };
    }
  }
];

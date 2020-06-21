//index.js

Page({
  data: {
    total_micro_seconds:0,
  },
  onLoad: function(options) {
    var that = this
    that.setData({
      total_micro_seconds:options.passabletime
    })
  }
})
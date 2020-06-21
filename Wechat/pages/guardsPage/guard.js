
function timeformat(hours,minutes,seconds) {
  var total_micro_seconds = (Number(hours*3600) + Number(minutes*60) + Number(seconds))*1000;
  /*console.log(hours);
  console.log(minutes);
  console.log(seconds);
  console.log(total_micro_seconds);*/
  return total_micro_seconds;
}
Page({
  data: {
    markers:[
      //示例markers
      {
        id:0,
        latitude:31.01809,
        longitude:121.43073,
      }
    ],
    latitude:31.01936,
    longitude:121.43021,
    clock:'',
    hours:0,
    minutes:0,
    seconds:0,
    total_micro_seconds:0,
  },

  onLoad:function(options) {
    var that = this
    
  },
  formSubmit:function(e){
    this.setData({
      hours:e.detail.value.hours,
      minutes:e.detail.value.minutes,
      seconds:e.detail.value.seconds,
    })
    //console.log(this.data.hours,this.data.minutes,this.data.seconds)
    var total_seconds = timeformat(this.data.hours,this.data.minutes,this.data.seconds);
    this.setData({
      total_micro_seconds:total_seconds,
    })
    console.log(this.data.total_micro_seconds)
    wx.navigateTo({
      url: '/pages/qrcode/qrcode?passabletime=' + this.data.total_micro_seconds,
    })
  },
})
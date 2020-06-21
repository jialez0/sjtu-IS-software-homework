var total_micro_second = 0;

function countdown(that){
  that.setData({
    clock:dateformat(total_micro_second)
  });

  if (total_micro_second <= 0) {
    return;
  }
  setTimeout(function(){
    total_micro_second -= 10;
    countdown(that);
  },10)
}

function dateformat(micro_second) {
  var second = Math.floor(micro_second/1000);
  var day = Math.floor(second / 3600/24);
  var hr = Math.floor(second / 3600);
  var hr2 = hr%24;
  var min = Math.floor((second - hr * 3600) / 60);
  var sec = (second - hr * 3600 - min * 60);// equal to => var sec = second % 60;
  return day+"天"+hr2 + "时" + min + "分" + sec + "秒" ;
}
Page({
  data: {
    markers:[],
    latitude:"",
    longitude:"",
    clock:'',
  },

  onLoad:function(options) {
    var that = this
    wx.getLocation({
      type:'wgs84',
      success: function (res) {
        console.log('纬度' + res.latitude);
        console.log('经度' + res.longitude);
        that.setData({
          latitude:res.latitude,
          longitude:res.longitude,
        })
      },
    })
    countdown(this);
  },
  scanCode:function() {
    wx.scanCode({
      complete: (res) => {
        console.log(res);
        total_micro_second = res.result;
      },
    })
  },
  onReady:function() {

  },
  onShow:function(){

  },
  onHide:function() {

  },
  onUnload:function(){

  },
  onPullDownRefresh:function() {

  },
  onReachBottome:function(){

  },
  onShareAppMessage:function(){

  }
})
//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        var postData = {
          code:res.code
        };
        wx.request({
          url: 'https://api.weixin.qq.com/sns/jscode2session?appid=wx4de30edc883b863f&secret=7d5f2e53de8b69b7d0980112e8e488ff&js_code='+res.code+'&grant_type=authorization_code',
          data:postData,
          method:'POST',
          success:function(res) {
            //console.log(res.data.openid);
            //wx.request({
            //  url: 'http://127.0.0.1:5000/wx/login',
            //  data:res.data.openid,
            //  method:'POST',
            //})
          },
        })
      }
    })
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.redirectTo({
            url: '../map/map',
          })
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo

              console.log(res.userInfo);
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  globalData: {
    userInfo: null
  }
})
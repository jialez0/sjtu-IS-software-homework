// pages/login/login.js
Page({

  data: {
  },

  LogIn:function(e){
    if(e.detail.value.password.length <6 ){

      wx.showToast({
  
      title: '密码小于6位！',  
      icon: 'none',
      duration: 1500
    })
  
    setTimeout(function(){
  
        wx.hideToast()
      },2000)
    } else if (e.detail.value.username != 'admin' || e.detail.value.password != '123456')
    { //在这里为了方便小程序独立测试，只验证用户名admin密码为123456的用户登录
      wx.showToast({
        title: '用户名密码错误',
        icon: 'none',
        duration: 1500
      })
      setTimeout(function(){
        wx.hideToast()
      },2000)
    } else{ 
      wx.redirectTo({
      url: '../guardsPage/guard',
    })
    // wx.request({
    //   url: 'http://127.0.0.1:5000/wx/login',
    //   data: {
    //   data: e.detail.value.username,
    //   password: e.detail.value.password
    //   },
    //   header: {
    //   'content-type': 'application/json' // 默认值
    //   },
    //   method:'POST',
    //   success:function(res) {
    //     if (res.data.status == '门卫') {
    //       wx.redirectTo({
    //        url: '../guardsPage/guard',
    //       })
    //     }
    //     else {
    //      wx.showToast({
    //        title: '用户名密码错误',
    //        icon: 'none',
    //        duration: 1500
    //      })
    //      setTimeout(function(){
    //        wx.hideToast()
    //      },2000)
    //     }
    //   }
    // })
    }
  }
})
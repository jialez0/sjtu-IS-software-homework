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
    {
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
    //   url: 'url',
    // })
    }
  }
})
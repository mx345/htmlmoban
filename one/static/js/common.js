"use strict";

$(function() {
    
    $("#uname").blur(function()
    {
        var uname = $(this).val();

        //用户格式校验
        if (uname.trim() ==="")
        {
            $("#uname_tips").css("color","red")
            $("#uname_tips").text("用户名不能为空")
            return;
        }

        if(/[\u4E00-\u9FFF]/.test(uname))
        {
            $("#uname_tips").css("color","red")
            $("#uname_tips").text("用户名不能为中文")
            return;
        }
        if (uname.length<4 ||uname.length>20 )
        {
            $("#uname_tips").css("color","red")
            $("#uname_tips").text("用户名最少为4字符！最大为20字符")
            return;
        }
        if (!/[a-zA-Z0-9_]+$/.test(uname))
        {

            $("#uname_tips").css("color","red")
            $("#uname_tips").text("用户名只能包含字母数字下划线")
            return;
        }
        $.ajax({
            url:"/check_uname",
            data:{
                uname:uname

            },
            success: function(data){
                if (data["err"]===0)
                {
                    //用户名没有被注册！
                    $("#uname_tips").css("color","green")
                    $("#uname_tips").css("font-width","bold")
                    $("#uname_tips").text("ok")  

                }
                else if (data["err"]===1)
                {
                    $("#uname_tips").css("color","red")
                    $("#uname_tips").text("用户户已被注册")
                }
                else
                {
                    
                }
            },
            error:function(){
            
            }
        })
    });
    var password
    $("#upass").blur(function()
    {
       password = $(this).val()
    
      if(password.length<6 ||password.length >15)
      {
        $("#upass_tips").css("color","red")
        
        $("#upass_tips").text("密码必须大于5，小于15！")
      }
      else{
        $("#upass_tips").css("color","green")
        $("#upass_tips").css("font-width","bold")
        $("#upass_tips").text("ok")  
      }
    })
    $("#upass2").blur(function()
    {   
        var password2= $(this).val()
        console.log(password2)
        console.log(password)
        if (password===password2)
        {   
            $("#upass2_tips").css("color","green")
            $("#upass2_tips").css("font-width","bold")
            $("#upass2_tips").text("ok")  

           
        }
        else{
            $("#upass2_tips").css("color","red")
            $("#upass2_tips").text("两次输入密码不一致！")
        }


    })
    $("#phone").blur(function()
    {   
        var phone= $(this).val()
       
        if(/1\d{10}/.test(phone))
        {   
            $("#phone_tips").css("color","green")
            $("#phone_tips").css("font-width","bold")
            $("#phone_tips").text("ok")  

           
        }
        else{
            $("#phone_tips").css("color","red")
            $("#phone_tips").text("手机号格式错误")
        }


    })
    $("#email").blur(function()
    {   
        var email= $(this).val()
        
        if(/^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/.test(email))
        {   
            $("#email_tips").css("color","green")
            $("#email_tips").css("font-width","bold")
            $("#email_tips").text("ok")  

           
        }
        else{
            $("#email_tips").css("color","red")
            $("#email_tips").text("邮箱格式错误")
        }


    })


    // $("#send_sms_code").click(function() {

    //     // 给服务器发送一个消息
    //     var phone = $("#phone").val();

    //     if(!/1\d{10}/.test(phone))
    //     {
    //         $("#phone_tips").css("color","red")
    //         $("#phone_tips").css("font-width","bold")
    //         $("#phone_tips").text("手机号码格式错误！")
    //         return;
    //     }
    //通过Ajax 将手机号发送给服务器后端程序

    //   $.ajax({
    //         type: "GET",
    //         url: "/phone",
    //         data:{
    //             email: email
    //         },
    //         success: function(data){
    //             if (data["err"]===0)
    //             {
    //                 //成功
                    
    //                 var s = 60;
    //                 $("#send_sms_code").prop("disabled", true);
    //                 $("#send_sms_code").html(s + "S");
                    
    //                 var timer = window.setInterval(function() {
    //                     --s;
    //                     if (s === 0) {
    //                         window.clearInterval(timer);
    //                         $("#send_sms_code").html("重新发送");
    //                         $("#send_sms_code").prop("disabled", false);
    //                         return;
    //                     }
            
    //                     $("#send_sms_code").html(s + "S");
    //                 }, 1000);

    //             }
    //             else
    //             {
    //                 alert("发送短信验证失败"+data["desc"])
    //             }

    //         },
    //         error: function () {           
    //             alert("发送请求失败,请检查网络连接！")
    //         }

    //   })
    
    });

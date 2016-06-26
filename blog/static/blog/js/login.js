$(function(){
    var user = $("#box_user")
    var pwd = $("#box_pwd")
    var pwd_again = $("#box_pwd_again")
    var img = $("#img_input")
    var captcha = $("#captcha")
    var msg = $("#msg")
    var btn_in = $("#btn_in")
    var btn_up = $("#btn_up");

    // 初始化`
    // 初始化输入字体颜色
    // 初始化文字
    (function(){
        msg.text("")
        user.val("账号")
        pwd.val("密码").attr("type","text")
        pwd_again.val("重复密码").attr("type","text")
        img.val("验证码")
        $("#box").find("input").css("color","#aaa")

    })();



    // 点击输入框 文字消失


    user.click(function(){
        if($(this).val()=="账号"){
            $(this).val("").removeAttr("style")
            
        }

    });

    pwd.click(function(){
        if ($(this).val()=="密码") {
            $(this).val("").removeAttr("style").attr("type","password")
        }
    });

    img.click(function(){
        if($(this).val()=="验证码"){
            $(this).val("").removeAttr("style")
        }
    });

    pwd_again.click(function(){
        if($(this).val()=="重复密码"){
            $(this).val("").removeAttr("style").attr("type","password")
        }
    });

    function cap_show(){
        captcha.attr("src","/blog/ajax_captcha/?flash="+Math.random())

    }

    captcha.click(cap_show)

    // 输入检测
    // 不为空检测
    function check(){
        if(!user.val() || user.val()=="账号"){
            msg.text("账号不能为空")
            user.val("账号").css("color","#aaa")
            cap_show()
        }else if(!pwd.val() || pwd.val()=="密码"){
            msg.text("密码不能为空")
            pwd.val("密码").css("color","#aaa").attr("type","password")
            cap_show()
        }else if(!img.val() || img.val() == "验证码"){
            msg.text("验证码不能为空")
            img.val("验证码").css("color","#aaa")
            cap_show()

        }else if($("#box_pwd_again").get(0)){
           if(!pwd_again.val() || pwd_again.val()=="重复密码"){
             console.log($("#box_pwd_again").get(0))
                msg.text("重复密码不能为空")
                pwd_again.val("重复密码").css("color","#aaa").attr("type","password")
                cap_show()
            }else if(pwd.val()!=pwd_again.val()){
                msg.text("两次密码输入不一致")
                cap_show()
            }else{
                msg.text("")
                return 1
            }

        }else{
            msg.text("")
            return 1
        }

        return 0
    }


    // 注册提交

    btn_up.click(function(){
        // console.log(pwd.val())
        msg.text("")

        var a =check()
        // 检测成功则发送ajax
        if(a){

            var username = user.val()
            
            var pwds = hex_md5(pwd.val())
            // console.log(pwds)
            var cap = img.val()

            function s_f(d){
                list_str = d.msg.split("|")
                if(list_str[0]=="ok"){
                    window.location.href="/blog/home/"
                }

                if(list_str[0]=="error"){
                    msg.text(list_str[1])
                    cap_show()
                }

            }
            ajax_log("/blog/ajax_logup",username,pwds,cap,s_f,function(){
                msg.text("注册失败")
                cap_show()
            })
        }

    })

    // 登陆提交
    btn_in.click(function(){
        msg.text("")
        var a=check()
        if(a){

            var username = user.val()
            var pwds = hex_md5(pwd.val())
            var cap = img.val()

            function s_f(d){
                list_str = d.msg.split("|")
                if(list_str[0]=="ok"){
                    window.location.href="/blog/home/"
                }

                if(list_str[0]=="error"){
                    msg.text(list_str[1])
                    cap_show()
                }

            }
            ajax_log("/blog/ajax_login/",username,pwds,cap,s_f,function(){
                msg.text("登陆失败")
                cap_show()
            })

        }
        // console.log(a)
    })






})
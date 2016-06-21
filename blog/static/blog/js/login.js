$(function(){
    var user = $("#box_user")
    var pwd = $("#box_pwd")
    var pwd_again = $("#box_pwd_again")
    var img = $(".img_input")
    var captcha = $("#captcha")

    function font_hidden(){

        $(this).val("")
        // alert($(this))
    }

    // 点击输入框 文字消失
    user.click(font_hidden);

    pwd.click(font_hidden);

    img.click(font_hidden);

    pwd_again.click(font_hidden);

    function cap_show(){
        $(this).attr("src","/blog/ajax_captcha/?flash="+Math.random())
    }

    captcha.click(cap_show)
})
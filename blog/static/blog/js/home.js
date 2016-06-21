$(function(){

    // 页面滚动 导航固定
    (function(){
        $(window).scroll(function(){
            if($(this).scrollTop() >= $("#head").height()){
                $("#nav").css({
                    "position":"fixed",
                    "top":"0",
                    "width":"100%",
                });

                $("#content").css({"padding-top":"90px"});

                }else{
                    $("#nav").css({
                        "position":"static"

                    });

                    $("#content").css({"padding-top":"30px"});
            }
        })

    })();

    // 注册登陆
    (function(){
        var log_in = $("#log_in")
        var log_up = $("#log_up")

        log_in.click(function(){
            
        })
    })();

})
$(function(){

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

    })()

})
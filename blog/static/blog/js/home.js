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

    // 页面查询返回标题列表
    var btn_list = $("#btn_list");
    var change_box=$("#change_box");

    btn_list.find("span").click(function(){
        value = $(this).text()
        data = {"article_class":value}
        ajax_titles(data,sf,ef)
        function sf(data){
            if(data.length<20){

                s = data.split("|")
                if(s[1]==undefined){
                    change_box.empty().append(data)
                }else{
                    alert(s[1])
                }

            }else{
                change_box.empty().append(data)
            }
        }

        function ef(){
            alert("服务器未响应")
        }
    })

})



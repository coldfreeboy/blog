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







    var change_box=$("#change_box");
    var pagecount = $("#pagecount")
    var pagenum = $("#pagenum")
    var page_jump = $("#page_jump")

    var btn_jump = $("#btn_jump")
    var btn_prev = $("#btn_prev")
    var btn_next = $("#btn_next")

    FINDDATA=[]
    FINDDATA[0]=""
     

    // 记录搜索关键此的全局变量
    // 查询总页数与请求html需要重复使用



    // 初次请求
    // 第一步查询总页码
    // 第二部请求html

    function title_page(data,page){

        ajax_titles(data,page,sf,ef)
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

                ajax_pagecount(FINDDATA[0],sf,ef)
                function sf(data){
                    if(data.length>5){
                        msg = data.split("|")
                        alert(msg[1])
                    }else{
                        pagecount.text(data)


                    }
                }

                function ef(){
                    alert("查询总页码服务器未响应")
                }
            }
        }

        function ef(){
            alert("服务器未响应")
        }

    }

    function first_request(){

        value = $(this).text()
        data = {"article_class":value}
        FINDDATA[0] =data
        // 请求html
        title_page(data,1)
    }

    

    // 页面查询返回标题列表
    var btn_list = $("#btn_list");
    
    btn_list.find("span").click(first_request)

    var btn_essay = $("#essay")
    btn_essay.click(first_request)

    // 翻页共能
    // 后翻页
    btn_next.click(function(){

        nownum = Number(pagenum.text())
        count = Number(pagecount.text())

        if(nownum>=count){
            num = count
        }else{
            num=nownum+1
        }
        ajax_titles(FINDDATA[0],num,sf,ef)
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
                pagenum.text(num)



                    }
        }

        function ef(){
            alert("查询总页码服务器未响应")
        }

    })

    btn_prev.click(function(){

        nownum = Number(pagenum.text())
        count = Number(pagecount.text())

        if(nownum<=1){
            num = 1
        }else{
            num=nownum-1
        }
        ajax_titles(FINDDATA[0],num,sf,ef)
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
                pagenum.text(num)


            }
        }

        function ef(){
            alert("服务器未响应")
        }

    })

    // 跳转命令

    btn_jump.click(function(){
        nownum = Number(page_jump.val())
        count = Number(pagecount.text())
        if(nownum>count || nownum<1){
            alert("页码超出范围")
            console.log(nownum)

        }else{

            ajax_titles(FINDDATA[0],nownum,sf,ef)
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
                    pagenum.text(nownum)


                }
            }

            function ef(){
                alert("服务器未响应")
            }

        }
    })





    // 搜索模块




    var search=$("#search")
    var search_data = $("#search_data")
    search.click(function(){
        data=search_data.val()

        dict = {title:data,keys:data}
        FINDDATA[0]=dict
        title_page(dict,1)
    })

})



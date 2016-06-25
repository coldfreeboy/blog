$(function(){
    // 编辑器
    var editor = new wangEditor("editor1");

        // 自定义菜单
    editor.config.menus = [
        'bold',
        'underline',
        'italic',
        'strikethrough',
        'eraser',
        'forecolor',
        'bgcolor',
        '|',
        'fontfamily',
        'fontsize',
        'unorderlist',
        'orderlist',
        'alignleft',
        'aligncenter',
        'alignright',
        '|',
        'link',
        'unlink',
        '|',
        'img',
        'insertcode',
        '|',
        'undo',
        'redo',
        'fullscreen'
     ];

    editor.create();

    
    



    // 文章内容获取并检查
    function article_save(sucess_fun,error_fun){
        title = $("#title").val()
        html = editor.$txt.html()
        tag = $("#tag option:selected").text()
        keys = $("#keys").val()
        id = $("#id").text()

        if(!title){
            alert("缺少标题")
        }else if(!html){
            alert("没有内容")
        }else if(!tag){
            alert("没有分类")
        }else if(!keys){
            alert("没有关键字")
        }else{
            // console.log(title)
            ajax_editor(title,html,tag,keys,id,sucess_fun,error_fun)
        }
    }



    var btn_submi = $("#btn_submit")
    btn_submi.click(function(){
        article_save(s_f,e_f);
        function s_f(data){
            str_list = data.split("|")
            if(str_list[0]=="ok"){
                window.location.href = "/blog/home/"
            }else{
                alert(str_list[1])
            }
        }

        function e_f(){
            alert("服务器未响应")
        }

    })






})
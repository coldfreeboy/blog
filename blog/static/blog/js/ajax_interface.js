  // ajax接口函数
  // 对应后台每个ajax请求
  // 每个函数最后两个参数为sfun,efun即成功后ajax回调函数和失败后ajax回调函数
  // sfun会有个参数data



// #登陆与注册
// url:登陆 /blog/ajax_login/
//     注册 /blog/ajax_logup/

// username 用户名
// pwd 密码
// cap 验证码

function ajax_log(url,username,pwd,cap,success_fn,error_fn){
    $.ajax({
        url:url,
        data:{"user":username,'pwd':pwd,"cap":cap},
        datatype:"json",
        type:"post",
        success:function(d){
            success_fn(d)

        },
        error:function(){
            error_fn()
        },

    })
}




// 文章编辑
// 参数:
// title 文章标题
// html  文章内容
// tag   文章分类
// keys  关键字
// id    空则新建文章 有id则修改id记录
function ajax_editor(title,html,tag,keys,id,fun,e_fun){

      $.ajax({
            url:"/blog/ajax_editor/",
            dataType:"text",
            type:"post",
            data:{"html":html,"title":title,"tag":tag,"keys":keys,"id":id},
            success:function(data){
                fun(data);

            },
            error:function(){
                e_fun();
            }

        }) 

}



// 删除按钮功能实现
// 参数
// id 要删除的文章id

function ajax_del(id,sfun,efun){
    $.ajax({
        url:"/blog/ajax_del/",
        dataType:"text",
        type:"post",
        data:{"id":id},
        success:function(data){
            sfun(data);

        },
        error:function(){
            efun();
        }

    }) 
}

// 文章查询
// 参数:
// arg: 对象数据类型
// 可用键:
// title
// keys
// 不用加__icontains

// user__username
// time
// article_class
// 需加__icontains实现包含查询
function ajax_titles(arg,sf,ef){
    datas=JSON.stringify(arg)
    $.ajax({
        url:"/blog/ajax_titles/",
        dataType:"text",
        type:"post",
        data:{"data":datas},
        success:function(data){
            sf(data);

        },
        error:function(){
            ef();
        }

    }) 
}

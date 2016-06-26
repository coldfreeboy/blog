# -*- coding: utf-8 -*-
import random
from io import BytesIO
from django.shortcuts import render,HttpResponse
from PIL import Image, ImageDraw, ImageFont,ImageFilter
import re
import json
from django import template 
from blog.models import Article
from django.db.models import Q



# 字库
FONT_PATH=u'./blog/static/blog/fonts/FreeSansBoldOblique.ttf'

class Captcha():

    '''

    验证码图片生成模块
    数字与字母随机产生
    初始化时第一个参数选择随机产生位数
    第二个参数选择生成图片长
    第三个参数选择生成图片高
    '''
    _letter_cases = u"abcdefghjkmnpqrstuvwxy" 
    _upper_cases = _letter_cases.upper()
    _numbers = u"".join(map(str,range(3,10)))
    init_chars = u"".join((_letter_cases,_numbers,_upper_cases,))
    def __init__(self,
                size=(130,40),
                length=4,
                chars=init_chars,
                img_type=u"gif",
                mode=u"RGB",
                bg_color=(255, 255, 255),
                fg_color=(0, 0, 255),
                font_size=30,
                font_type=FONT_PATH,
                draw_lines=True,
                n_line=(2, 3),
                draw_points=True,
                point_chance = 2):
        '''
        @todo: 生成验证码图片
        @param size: 图片的大小，格式（宽，高），默认为(120, 30)
        @param chars: 允许的字符集合，格式字符串
        @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
        @param mode: 图片模式，默认为RGB
        @param bg_color: 背景颜色，默认为白色
        @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
        @param font_size: 验证码字体大小
        @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
        @param length: 验证码字符个数
        @param draw_lines: 是否划干扰线
        @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
        @param draw_points: 是否画干扰点
        @param point_chance: 干扰点出现的概率，大小范围[0, 100]
        @param img:初始化绘制图形
        @param draw:初始化画笔
        @return: [0]: PIL Image实例
        @return: [1]: 验证码图片中的字符串
        '''
        self.size=size
        self.chars=chars
        self.img_type=img_type
        self.mode=mode
        self.bg_color=bg_color
        self.fg_color=fg_color
        self.font_size=font_size
        self.font_type=font_type
        self.length=length
        self.draw_lines=draw_lines
        self.n_line=n_line
        self.draw_points=draw_points
        self.point_chance=point_chance
        self.img = Image.new(mode,size,bg_color)
        self.draw = ImageDraw.Draw(self.img)
        self.strs = None


    def get_chars(self):
        """
        生成随机字符，返回字符
        """
        
        return u"".join(self.strs)
    
    def _creat_lines(self):
        "绘制干扰线"
        line_num =random.randint(*self.n_line)

        for i in range(line_num):
            a=random.randint(0,256)
            b=random.randint(0,256)
            c=random.randint(0,256)

            begin = (random.randint(0, int(self.size[0]/3)), random.randint(0, self.size[1]))
            end = (random.randint(int(self.size[0]/3), self.size[0]), random.randint(0, self.size[1]))
            self.draw.line([begin,end],fill=(a,b,c))    
    
    def _create_points(self):
        "绘制干扰点"
        chance = min(100,max(0,int(self.point_chance)))#大小限制在[0,100]

        for w in range(self.size[0]):
            for h in range(self.size[1]):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    a=random.randint(64,255)
                    b=random.randint(64,255)
                    c=random.randint(64,255)
                    self.draw.point((w, h), fill=(a, b, c))

    def _creat_strs(self):



        self.strs = random.sample(self.chars,self.length)
        font = ImageFont.truetype(self.font_type, self.font_size)
        num=0
        for i in range(self.length):
            a=random.randint(32,255)
            b=random.randint(32,255)
            c=random.randint(32,255)
            x = (int(self.size[0])/self.length)*num+(self.size[0]-self.font_size*self.length)/2
            y = random.choice([(int((self.size[1])-self.font_size)/2),0,int((self.size[1])-self.font_size)])
            self.draw.text((x, y),self.strs[num], font=font, fill=(a,b,c))
            num=num+1

    
    def creat(self):
        '''
        生成图片并返回
        '''
        self._creat_strs()
        if self.draw_lines:
            self._creat_lines()
        if self.draw_points:
            self._create_points()

        self.img=self.img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）
        return self.img

    def get_byte(self):
        # 转换成比特用以传输给前端
        buf = BytesIO()
        self.img.save(buf,self.img_type)
        bimg = buf.getvalue()
        return bimg


# ajax 字典数据解析
def ajax_dict(request,key):
    """
    ajax传进来的字典数据 进行获取和json反序列化

    """
    try:
        data = request.POST.get(key)
    except Exception as e:
        print(e)
        raise Exception("error|获取失败")
    else:
        data = json.loads(data)
    return data

 
def check_post(f):
    """
    检查post的装饰器

    """

    def call(request, *arg, **args):
        if request.method=="POST":
            return f(request, *arg, **args)
        else:
            return HttpResponse("<h1>错误:请使用post</h1>")
    return call

def check_login(f):
    def call(request, *arg, **args):
        if request.user.is_authenticated():
            return f(request, *arg, **args)
        else:
            return HttpResponse("<h1>您未登录!</h1>")

    return call

def re_js(text):
    old_left=u"<script>"
    old_right = u"</script>"

    new_left = u"&lt;script&gt;"
    new_right = u"&lt;/script&gt;"

    result_str = re.sub(old_left,new_left,text)
    result_str = re.sub(old_right,new_right,result_str)
    return result_str


# 生成文章标题列表
def create_html(request,obj):
    html=u"""
        {% for i in obj %}
            <div>
                <p><a href="/blog/show_article/{{i.id}}/" target="_blank">{{i.title|safe}}</a></p>
                <span>作者:{{i.user}}</span>
                <span>分类:{{i.article_class}}</span>
                <span>关键字:{{i.keyword}}</span>
                {# 验证是否为登陆用户,是则显示操作按钮#}
                {% if user.id == i.user.id %}
                    <span class="button"><a href="/blog/editor_article/{{i.id}}" target="_blank">编辑</a></span>
                    <span class="button del">删除</span>
                {% endif %}
            </div>
            <hr>
        {% endfor %}
        {% if user %}
            <script>

        
                $(".del").click(function(){
                    del_obj = $(this).parent()
                    ids = del_obj.find("a").first().attr("href")
                    id = ids.split("/")[3]
                    change_box = $("#change_box")

                    
                    finddata = FINDDATA[0]
                    page = $("#pagenum")
                    pagecount = $("#pagecount")

                    ajax_del(id,sf,ef)

                    function sf(data){
                        list_msg = data.split("|")

                        alert(list_msg[1])


                        jump(finddata,Number(page.text()),change_box)
                    }

                    function ef(){
                        alert("服务器未响应1111")
                    }
                })
                
            </script>
        {% endif %}

    """
    t = template.Template(html)
    c = template.Context({"obj":obj,"user":request.user})
    return t.render(c)

def find_data(data):

    # 根据查询关键字返回搜索到的数据集
    if len(data)==1:
        try:
            obj = Article.objects.filter(**data)

        except Exception as e:
            msg="error|数据库获取失败"
            print("%s'|'%s"%(msg,e))
        else:
            return obj

    elif len(data)==2:

        v1 = data[u"title"]
        v2 = data[u"keys"]
        print(data)
        q1 = Q(title__icontains=v1)
        q2 = Q(keyword__icontains=v2)

        try:
            obj = Article.objects.filter(q1 | q2)
        except Exception as e:
            msg="error|数据库获取失败"
            print("%s'|'%s"%(msg,e))
        else:
            return obj

    else:
        return Article.objects.all()

# 总页数及所需也的obj生成
class Page():
    def __init__(self,database=Article.objects.all(),max_title=10):

        # 操作集及每页记录数
        self.base = database
        self.num_onepage = max_title

    def page_count(self):
        """
        总页数
        """

        # 总文章数
        num_count = self.base.count()


        if num_count == 0:
            return 0

        if num_count <= self.num_onepage:
            return 1

        # 总页数  地板除  
        page_c = int(num_count//self.num_onepage)
        # 是否整除,没整除则还有一页
        last =  1 if num_count%self.num_onepage else 0 

        return page_c+last

    def page_obj(self,page_num):
        """
        所需页的对象
        """
        # 所需对象索引
        nextpage = page_num*self.num_onepage
        prevpage = nextpage - self.num_onepage


        try:
            obj = self.base[prevpage:nextpage]
        except Exception as e:
            msg="error|数据库页码对象获取失败"
            print("%s'|'%s"%(msg,e))

        else:
            return obj








        








    

# -*- coding: utf-8 -*-
import random
from io import BytesIO
from django.shortcuts import render,HttpResponse
from PIL import Image, ImageDraw, ImageFont,ImageFilter

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





def resolve(request,key,t):
    """
    request.POSt的数据解析
    key:要解析的键
    t:要解析的类型 dict str int 等
    """
    import json
    try:
        data = request.POST.get(key)
    except Exception as e:
        print(e)
        raise Exception("error|获取失败")
    else:
        if data or data ==u"" or data == 0:
            try:
                if t==dict:
                    data = json.loads(data)
                    args={}
                    for key,value in data.iteritems():
                        if value == u"False" or value==u"false":
                            args[key]=False
                        elif value == u"True" or value ==u"true":
                            args[key]=True
                        else:
                            args[key]=value 
                    return args

                else:
                    data = t(data)
                
            except Exception as e:
                print(e)
                raise Exception("error|转化失败")
            else:
                return data
        else:
            raise Exception("error|原始数据解析失败")



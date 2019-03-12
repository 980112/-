from django.shortcuts import render, redirect, HttpResponse
from check.models import Userinfo
from PIL import Image, ImageDraw, ImageFont
from django.http import JsonResponse
from io import BytesIO
import random


# Create your views here.

def get_valid_img(request):
    def get_white():
        return (255, 255, 153)

    #  生成随机颜色
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # 生成随机背景色的图片
    img = Image.new('RGB', (112, 37), get_white())
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('static/font/kumo.ttf', 32)

    code = ""  # 验证码明文
    # 生成随机验证码
    for i in range(4):
        random_num = str(random.randint(0, 9))  # 生成随机数字
        random_up = chr(random.randint(65, 90))  # 生成随机大写字母
        random_low = chr(random.randint(97, 122))  # 生成随机小写字母

        # 随机选择数字,大写字母,小写字母中的一个
        random_char = random.choice([random_low, random_up, random_num])

        # 在生成的随机背景色图片上绘制随机颜色的随机验证码
        draw.text((i * 25 + 10, 0), random_char, get_random_color(), font=font)

        # 保存生成的随机验证码
        code += random_char
    print("验证码是: ", code)

    width = 112
    height = 37
    # 添加噪线
    for i in range(2):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    # 添加噪点
    for i in range(20):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # 将生成的验证码图片保存在内存中
    f = BytesIO()  # 句柄
    img.save(f, 'png')  # 保存
    data = f.getvalue()  # 验证码图片数据

    # 将验证码保存在各自的session中,方便不同浏览器之间进行验证
    request.session['code'] = code

    return HttpResponse(data)


# 登录
def login(request):
    if request.method == "GET":
        static = request.session.get("static")
        if static:
            return redirect('/homepage/')
        return render(request, "login.html")

    if request.is_ajax():
        user = request.POST.get('user')
        pwd = request.POST.get("pwd")
        code = request.POST.get("code")
        print('账号: ', user, '密码: ', pwd, '验证码: ', code)

        ret = {'static': False, 'err_msg': ""}

        if code.upper() == request.session.get('code').upper():
            user_obj = Userinfo.objects.filter(user=user, pwd=pwd).first()
            if user_obj:
                request.session['username'] = user
                request.session['static'] = True
                ret['static'] = True
            else:
                ret['err_msg'] = '账号或密码错误'
        else:
            ret['err_msg'] = '验证码错误'

        return JsonResponse(ret)


def logout(request):
    request.session.flush()
    return redirect('/login/')


# 注册
def register(request):
    return render(request, 'register.html')


# 主页
def homepage(request):
    static = request.session.get("static")
    print(static)
    if not static:
        return redirect('/login/')
    user = request.session.get('username')
    return render(request, 'homepage.html', locals())

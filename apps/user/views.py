from django.shortcuts import render , redirect
import re
from user.models import MyUser,Address
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import View
from django.core.mail import send_mail
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from itsdangerous import TimedJSONWebSignatureSerializer as TJWS  #引入加密函数
from itsdangerous import SignatureExpired,BadSignature  #引入加密函数
from utils.celery.tasks import send_register_active_email
from django.contrib.auth import authenticate,login

# Create your views here.
# 使用内置视图
# def register(request):
#     """注册页"""
#     #第一种写法
#     if request.method == 'GET':
#         return render(request, "user/register.html")
#     elif request.method == 'POST':
#         username = request.POST.get('user_name')
#         password = request.POST.get('pwd')
#         email = request.POST.get('email')
#         allow = request.POST.get('allow')
#         # 验证
#         if not all([username, password, email]):
#             return render(request, "user/register.html", {'errmsg': '数据不完整'})
#         if re.match('/^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/', email):
#             return render(request, "user/register.html", {'errmsg': '邮箱格式 不正确'})
#         if allow != 'on':
#             return render(request, "user/register.html", {'errmsg': '请同意用户协议'})
#         # 检测用户名信息 是否存在
#         try:
#             user = MyUser.objects.get(username=username)
#         except MyUser.DoesNotExist:
#             user = None
#         # 业务处理
#         '''第一种创建方式'''
#         # user = MyUser()
#         # user.username = username
#         # user.password = password
#         # user.email = email
#         # user.save()
#
#         if user:
#             return render(request, "user/register.html", {'errmsg': '用户名已经存在'})
#         else:
#             user = MyUser.objects.create_user(username, email, password)
#         if user == True:
#             pass
#         # return render(request, "user/register.html")
#         return redirect(reverse('goods:index'))
#     #使用类视图
def register_submit(request):
    '''接受数据'''
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    #验证
    if not all([username,password,email]):
        return render(request, "user/register.html",{'errmsg':'数据不完整'})
    if re.match('/^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/',email):
        return render(request, "user/register.html", {'errmsg': '邮箱格式 不正确'})
    if allow != 'on':
        return render(request, "user/register.html", {'errmsg': '请同意用户协议'})
    #检测用户名信息 是否存在
    try:
        user = MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        user = None
    #业务处理
    '''第一种创建方式'''
    # user = MyUser()
    # user.username = username
    # user.password = password
    # user.email = email
    # user.save()

    if  user:
        return render(request, "user/register.html", {'errmsg': '用户名已经存在'})
    else:
        user = MyUser.objects.create_user(username, email, password)
    if user == True:
        pass
    # return render(request, "user/register.html")
    return redirect(reverse('goods:index'))
    #返回应答

'''类视图'''
class RegisterView(View):
    def get(self,request):
        return render(request, "user/register.html")
    def post(self,request):
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 验证
        if not all([username, password, email]):
            return render(request, "user/register.html", {'errmsg': '数据不完整'})
        if re.match('/^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/', email):
            return render(request, "user/register.html", {'errmsg': '邮箱格式 不正确'})
        if allow != 'on':
            return render(request, "user/register.html", {'errmsg': '请同意用户协议'})
        # 检测用户名信息 是否存在
        try:
            user = MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            user = None
        # 业务处理
        '''第一种创建方式'''
        # user = MyUser()
        # user.username = username
        # user.password = password
        # user.email = email
        # user.save()

        if user:
            return render(request, "user/register.html", {'errmsg': '用户名已经存在'})

        user = MyUser.objects.create_user(username, email, password)
            #发送激活链接
        if user == True:
            pass
        # TJWS_ss = TJWS(settings.SECRET_KEY, 7200)
        # info = {'username': username}
        # token = TJWS_ss.dumps(info)
        rec = ['571666271@qq.com']
        send_register_active_email.delay(username)
        # token = token.decode('utf-8')
        # subject = '{},天天生鲜欢迎您'.format(username)
        # message = '天天生鲜欢迎您,{}'.format(username)
        # send = settings.EMAIL_FROM
        # rec = ['571666271@qq.com']
        # html_message = '<h1>欢迎您注册天天生鲜</h1>，请点击下面连接进行激活<br /><a href="http://123.206.27.175:8001/user/active/{}">http://123.206.27.175:8001/user/active/{}</a>'.format(username,token,token)
        # send_mail(subject, message, send, rec,html_message=html_message)
        # return render(request, "user/register.html")
        return redirect(reverse('goods:index'))
    def active_email_send(self):
        pass

class ActiveView(View):
    def get(self,request,token):
        #解密
        TJWS_re = TJWS(settings.SECRET_KEY,7200)
        try:
            # token = token.decode('utf-8')
            # info = TJWS_re.loads(token)
            # username = info['username']
            #token 发送时候 未进行加密
            username = token
            user = MyUser.objects.get(username=username)
            user.is_active = True
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已经过期')
        except BadSignature:
            return HttpResponse('无效激活码？{}'.format(token))
class LoginView(View):
    def get(self,request):
        return render(request, "user/login.html")
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if not all([username,password]):
            return render(request, "user/login.html", {'errmsg': '数据不完整'})

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                #用户已经激活
                login(request,username)
                return redirect(reverse('goods:index'))
            else:
                #用户 未激活
                return render(request, "user/login.html", {'errmsg': '请先激活账号'})
        else:
            return render(request, "user/login.html", {'errmsg': '账号或密码错误'})
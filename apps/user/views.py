from django.shortcuts import render , redirect
import re
from user.models import MyUser,Address
from django.urls import reverse
from django.middleware.csrf import CsrfViewMiddleware
# Create your views here.

def register(request):
    """注册页"""
    return render(request, "user/register.html")
    # if request.method == "GET":  # 如果请求方式是GET请求 代表请求注册页面
        # context["user"] = None  # 初始化模板user参数为None
        # context["captcha"] = forms.Check_Code()  # 传递验证码 直接返回模板
        # return render(request, "user/register.html")
    # elif request.method == "POST":
    #     return render(request, "user/login.html")
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
    #业务处理
    '''第一种创建方式'''
    # user = MyUser()
    # user.username = username
    # user.password = password
    # user.email = email
    # user.save()
    user = MyUser.objects.create_user(username,email,password)
    if user == True:
        pass
    # return render(request, "user/register.html")
    return redirect(reverse('goods:index'))
    #返回应答

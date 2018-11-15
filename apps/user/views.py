from django.shortcuts import render , redirect
import re
from user.models import MyUser,Address
# from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import View
from django.middleware.csrf import CsrfViewMiddleware
# Create your views here.
# 使用内置视图 
def register(request):
    """注册页"""
    #第一种写法
    if request.method == 'GET':
        return render(request, "user/register.html")
    elif request.method == 'POST':
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
        else:
            user = MyUser.objects.create_user(username, email, password)
        if user == True:
            pass
        # return render(request, "user/register.html")
        return redirect(reverse('goods:index'))
    #使用类视图
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
        else:
            user = MyUser.objects.create_user(username, email, password)
        if user == True:
            pass
        # return render(request, "user/register.html")
        return redirect(reverse('goods:index'))
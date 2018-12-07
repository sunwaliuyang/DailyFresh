from django.shortcuts import render , redirect
import re
from user.models import MyUser,Address
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from django.views.generic import View
from django.core.mail import send_mail
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from itsdangerous import TimedJSONWebSignatureSerializer as TJWS  #引入加密函数
from itsdangerous import SignatureExpired,BadSignature  #引入加密函数
from utils.celery.tasks import send_register_active_email
from django.contrib.auth import authenticate,login,logout
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
from goods.models import GoodsSku
from order.models import OrderInfo,OrderGoods
from django.core.paginator import Paginator


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
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        # 使用模板
        return render(request, 'user/login.html', {'username': username, 'checked': checked})
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if not all([username,password]):
            return render(request, "user/login.html", {'errmsg': '数据不完整'})

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                #用户已经激活
                login(request,user)

                # 获取登录后所要跳转到的地址
                # 默认跳转到首页
                next_url = request.GET.get('next', reverse('goods:index'))

                # 跳转到next_url
                response = redirect(next_url)  # HttpResponseRedirect

                #判断是否需要记录用户信息
                remember = request.POST.get('remember')

                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                return response
            else:
                #用户 未激活
                return render(request, "user/login.html", {'errmsg': '请先激活账号'})
        else:
            return render(request, "user/login.html", {'errmsg': '账号或密码错误'})

class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        address = Address.objects.get_default_address(user)
        #获取用户浏览记录
        #浏览记录  记录在redis
        con = get_redis_connection("default")
        history_key = "history_%d"%user.id
        sku_ids = con.lrange(history_key,0,4)
        # 从数据库中查询用户浏览的商品的具体信息
        # goods_li = GoodsSku.objects.filter(id__in=sku_ids)
        #
        # goods_res = []
        # for a_id in sku_ids:
        #     for goods in goods_li:
        #         if a_id == goods.id:
        #             goods_res.append(goods)

        #便利获取用户浏览的商品信息
        goods_li = []
        for id in sku_ids:
            goods = GoodsSku.objects.get(id=id)
            goods_li.append(goods)
        # 组织上下文
        context = {
            'page':'user',
            "address":address,
            'goods_li':goods_li
        }
        return render(request,'user/user_center_info.html',context)

class UserOrderView(LoginRequiredMixin,View):
    def get(self, request,page):
        '''显示'''
        # 获取用户的订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        # 遍历获取订单商品的信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            # 遍历order_skus计算商品的小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count * order_sku.price
                # 动态给order_sku增加属性amount,保存订单商品的小计
                order_sku.amount = amount

            # 动态给order增加属性，保存订单状态标题
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            # 动态给order增加属性，保存订单商品的信息
            order.order_skus = order_skus

        # 分页
        paginator = Paginator(orders, 1)
        # page = request.GET.get('page')
        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        order_page = paginator.page(page)

        # todo: 进行页码的控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 组织上下文
        context = {'order_page': order_page,
                   'pages': pages,
                   'page': 'order'}

        # 使用模板
        return render(request, 'user/user_center_order.html', context)
class UserSiteView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        addr = Address.objects.get_default_address(user)
        return render(request,'user/user_center_site.html',{'page':'address','address':addr})
    def post(self,request):
        # 接收数据
        receiver = request.POST.get('receiver')
        address = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 校验数据
        if not all([receiver, address, phone]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})

        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8|6][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})

        # 业务处理：地址添加
        # 如果用户已存在默认收货地址，添加的地址不作为默认收货地址，否则作为默认收货地址
        # 获取登录用户对应User对象
        user = request.user

        # try:
        #     addr = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在默认收货地址
        #     addr = None
        addr = Address.objects.get_default_address(user)

        if addr:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               address=address,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        # 返回应答,刷新地址页面
        return redirect(reverse('user:address'))  # get请求方式

# /user/logout
class LogoutView(View):
    '''退出登录'''
    def get(self, request):
        '''退出登录'''
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('goods:index'))
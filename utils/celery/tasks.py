#引入
from celery import Celery,shared_task
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as TJWS  #引入加密函数
from itsdangerous import SignatureExpired,BadSignature  #引入加密函数
# import celeryconfig
import time
from fresh.celery import app
# app = Celery("utils.celery",broker='redis://123.206.27.175:6379/1')
# redis://:password@hostname:port/db_number
# app = Celery("utils.celery",broker='redis://:liuyang506@123.206.27.175:6379/1')
# Celery("utils.celery",broker='redis://**********:6379/1')
# app = Celery('utils.celery')
# 从单独的配置模块中加载配置
# app.config_from_object('celeryconfig')
#定义任务函数
# @app.shared_task
# def send_register_active_email(username):
#     subject = '{},天天生鲜欢迎您'.format(username)
#     message = '天天生鲜欢迎您,{}'.format(username)
#     TJWS_ss = TJWS(settings.SECRET_KEY, 7200)
#     info = {'username': username}
#     token = TJWS_ss.dumps(info)
#     send = settings.EMAIL_FROM
#     rec = ['571666271@qq.com']
#     html_message = '<h1>欢迎您注册天天生鲜</h1>，请点击下面连接进行激活<br /><a href="http://123.206.27.175:8001/user/active/{}">http://123.206.27.175:8001/user/active/{}</a>'.format(
#         username, token, token)
#     send_mail(subject, message, send, rec, html_message=html_message)\
@app.task
def send_register_active_email(username):
    subject = '{},天天生鲜欢迎您'.format(username)
    message = '天天生鲜欢迎您,{}'.format(username)
    TJWS_ss = TJWS(settings.SECRET_KEY, 7200)
    info = {'username': username}
    token = TJWS_ss.dumps(info)
    send = settings.EMAIL_FROM
    rec = ['571666271@qq.com']
    html_message = '<h1>欢迎您注册天天生鲜</h1>，请点击下面连接进行激活<br /><a href="http://123.206.27.175:8001/user/active/{}">http://123.206.27.175:8001/user/active/{}</a>'.format(
        username, token, token)
    send_mail(subject, message, send, rec, html_message=html_message)

@app.task
def my_tast_beat():
    return time.time()


@app.task
def generate_static_index_html():
    '''产生首页静态页面'''
    # 获取商品的种类信息
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    for type in types:  # GoodsType
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners


    # 组织模板上下文
    context = {'types': types,
               'goods_banners': goods_banners,
               'promotion_banners': promotion_banners}

    # 使用模板
    # 1.加载模板文件,返回模板对象
    temp = loader.get_template('static_index.html')
    # 2.模板渲染
    static_index_html = temp.render(context)

    # 生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR, 'templates/static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_index_html)


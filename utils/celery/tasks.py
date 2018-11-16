#引入
from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as TJWS  #引入加密函数
from itsdangerous import SignatureExpired,BadSignature  #引入加密函数
# app = Celery("utils.celery",broker='redis://123.206.27.175:6379/1')
# redis://:password@hostname:port/db_number
app = Celery("utils.celery",broker='redis://[:liuyang506]@123.206.27.175:6379/1')
# Celery("utils.celery",broker='redis://**********:6379/1')

#定义任务函数
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
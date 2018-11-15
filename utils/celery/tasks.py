#引入
from celery import Celery

#创建实例

Celery("utils.celery",broker='redis://**********:6379/1')

#定义任务函数
def sen_register_active_email(to_email,username,token):
    pass
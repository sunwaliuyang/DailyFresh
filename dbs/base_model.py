from django.db import models

'''抽象模型类'''
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    is_delete = models.BooleanField(default=False,verbose_name='是否删除')
    class Meta:
        #说明这是一个抽象类
        abstract = True
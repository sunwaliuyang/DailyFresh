from django.db import models
from dbs.base_model import BaseModel
from django.contrib.auth import get_user_model
from django.conf import settings
# User = get_user_model()
# Create your models here.
class OrderInfo(BaseModel):
    '''订单模型类'''
    PAY_TYPE_CHOICES = (
        (0,'货到付款'),
        (1,'微信支付'),
        (2,'支付宝'),
        (3,'银联支付'),
        (4,'信用卡支付'),
    )
    ORDER_STATUS_CHOICES = (
        (0,'待支付'),
        (1,'支付中'),
        (2,'已支付'),
        (3,'支付失败'),
        (4, '待发货'),
        (5, '发货中'),
        (6, '已发货'),
        (7, '待收货'),
        (8, '已收货'),
        (9, '待评价'),
        (10, '已完成'),
    )
    order_id = models.CharField(max_length=128,primary_key=True,verbose_name='订单ID')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='MyUser_username',on_delete=models.CASCADE,verbose_name='用户')
    address = models.ForeignKey('user.Address',on_delete=models.CASCADE,verbose_name='地址')
    pay_method = models.SmallIntegerField(default=2,choices=PAY_TYPE_CHOICES,verbose_name='支付方式')
    total_count = models.IntegerField(default=1,verbose_name='商品数量')
    total_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品总价')
    transit_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='订单运费')
    order_status = models.SmallIntegerField(default=0,choices=ORDER_STATUS_CHOICES,verbose_name='订单状态')
    trade_no = models.CharField(max_length=128,verbose_name='支付编号')

    class Meta:
        db_table = 'df_order_info'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name
class OrderGoods(BaseModel):
    '''订单商品模型类'''
    order = models.ForeignKey("OrderInfo",on_delete=models.CASCADE,verbose_name='订单')
    sku = models.ForeignKey("goods.GoodsSku",on_delete=models.CASCADE,verbose_name='商品SKU')
    count = models.IntegerField(default=1,verbose_name='商品数量')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品价格')
    comment = models.CharField(max_length = 128,verbose_name='评论')

    class Meta:
        db_table = 'df_order_goods'
        verbose_name = '订单商品信息'
        verbose_name_plural = verbose_name
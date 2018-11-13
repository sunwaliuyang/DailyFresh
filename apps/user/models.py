from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.auth import get_user_model
from itsdangerous import TimedJSONWebSignatureSerializer as TJWS
from dbs.base_model import BaseModel
# Create your models here
class MyUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        return self._create_user(username, email, password, **extra_fields)
class MyUser(AbstractBaseUser,BaseModel,PermissionsMixin):
    # #用户模型类
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )
    username = models.CharField('username', max_length=20, unique=True, db_index=True)
    password = models.CharField('password', max_length=128,db_index=True)
    birthday = models.DateField("出生年月", null=True, blank=True)
    gender = models.CharField("性别", max_length=6, choices=GENDER_CHOICES, default="female")
    mobile = models.CharField("电话", max_length=11, null=True, blank=True, help_text='手机号')
    email = models.EmailField("邮箱", max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','password']
    objects = MyUserManager()
    def generate_active_token(self):
        '''生产用户签名字符串'''
        serializer = TJWS(settings.SECRET_KEY,3600)
        info = {'confirm':self.id}
        token = serializer.dumps(info)
        return token.decode()
    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
class Address(BaseModel):
    '''地址模型类'''
    user = models.ForeignKey('MyUser',on_delete=models.CASCADE,verbose_name='所属账户')
    receiver = models.CharField(max_length=32,verbose_name='收件人')
    address = models.CharField(max_length=256,verbose_name='收件地址')
    zip_code = models.CharField(max_length=6,null=True,verbose_name='邮编')
    phone = models.CharField(max_length=11,verbose_name='联系电话')
    is_default = models.BooleanField(default=False,verbose_name='是否默认')

    class Meta:
        db_table = 'df_address'
        verbose_name = ''
        verbose_name_plural = verbose_name

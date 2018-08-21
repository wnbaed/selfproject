# _*_coding:UTF-8_*_
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nick_name= models.CharField(max_length=50,verbose_name=u'用户名'
                                ,default='')
    birthday = models.DateField(verbose_name='生日',blank=True,null=True)
    gender = models.CharField(verbose_name='性别',max_length=7,choices=(('male',u'男'),
    ('female',u'女')),default='female')
    address = models.CharField(verbose_name='地址',blank=True,null=True,
                               max_length=100,default='')
    mobile = models.CharField(verbose_name='手机',max_length=11,default='',
                              null=True,blank=True)
    image = models.ImageField(verbose_name='头像',max_length=100,
                             upload_to='image/%Y/%m')
    class Meta:
        verbose_name='用户信息'
        verbose_name_plural= verbose_name
    def __str__(self):
        return  self.username

class EmailVarifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name='验证码')
    email = models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type = models.CharField(verbose_name='验证码类型',choices=(('register',u'注册'),('forget',u'找回密码')),max_length=10)
    send_time = models.DateTimeField(verbose_name='发送时间',default=datetime.now)

    class Meta:
        verbose_name =  '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email

class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m',verbose_name='轮播图')
    url = models.URLField(max_length=200,verbose_name=u'访问地址')
    index = models.IntegerField(default=100,verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    class Meta:
        verbose_name=u'轮播图'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title
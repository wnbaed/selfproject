# _*_coding:UTF-8_*_
from datetime import datetime
from django.db import models



# Create your models here.
class CityDict(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'城市')
    desc = models.CharField(max_length=200,verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name=u"城市"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

class CourseOrg(models.Model):
    name = models.CharField(max_length=50,verbose_name=u'机构名称')
    category = models.CharField(verbose_name=u'机构类别',max_length=20,choices=(('pxjg','培训机构'),('gr','个人'),('gx','高校')),default='pxjg')
    desc = models.TextField(verbose_name=u'机构描述')
    students = models.IntegerField(verbose_name=u'学习人数',default=0)
    course_nums = models.IntegerField(verbose_name=u'课程数',default=0)
    click = models.IntegerField(default=0,verbose_name=u'点击数')
    image = models.ImageField(upload_to='org/%Y/%m',verbose_name=u'logo',max_length=100,blank=True)
    address =models.CharField(max_length=150,verbose_name=u'机构地址')
    # 城市外键
    city = models.ForeignKey(CityDict,verbose_name=u'所在城市')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name='课程机构'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

class Teacher(models.Model):
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'教师头像', max_length=100, blank=True)
    org = models.ForeignKey(CourseOrg,verbose_name=u'所属机构')
    name = models.CharField(max_length=50,verbose_name=u'教师名')
    work_year = models.IntegerField(default=0,verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50,verbose_name=u'就职公司')
    work_position =  models.CharField(max_length=50,verbose_name=u'公司职位')
    points = models.CharField(max_length=50,verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏数')
    add_time = models.DateTimeField(default=datetime.now)



    class Meta:
        verbose_name=u'教师'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

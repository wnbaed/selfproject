# _*_ encoding:utf-8_*_
from datetime import datetime
from django.db import models
from organization.models import CourseOrg,Teacher
# Create your models here.


class Course(models.Model):
    teacher = models.ForeignKey(Teacher,verbose_name='教师',blank=True,null=True)
    courseorg = models.ForeignKey(CourseOrg,verbose_name=u'课程机构',blank=True,null=True)
    name = models.CharField(max_length=50,verbose_name='课程名')
    desc = models.CharField(max_length=300,verbose_name='课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.TextField(verbose_name=u'难度',choices=(('cj','初级'),('zj','中级'),('gj','高级')),max_length=2)
    learn_times = models.IntegerField(default=0,verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name=u'封面图',max_length=100,blank=True)
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    category = models.CharField(default=0,verbose_name='课程类别',max_length=20)
    tag = models.CharField(default='',verbose_name=u'课程标签',max_length=10,blank=True)
    youneed_know = models.CharField(max_length=300,verbose_name='课程须知',default='')
    teacher_tell = models.CharField(max_length=300,verbose_name='教师提醒',default='')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name=u'课程'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name
    def get_zj_nums(self):
        #获取课程章节数
        return self.lesson_set.all().count()
    def get_learn_users(self):
        # 获取课程学习人数
        return self.usercourse_set.all()

class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name =u'章节'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u'章节')
    name = models.CharField(max_length=100,verbose_name='视频名')
    url = models.CharField(max_length=200, verbose_name=u'访问地址', default='')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name=u'视频'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u'资源名称')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    download = models.FileField(upload_to='coures/resource/%Y/%m',verbose_name=u'资源文件',max_length=100)

    class Meta:
        verbose_name=u'课程资源'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name
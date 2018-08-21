# _*_coding:utf-8_*_

import xadmin
from .models import *

class CourseAdmin(object):
    # 内容展现字段
    list_display = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    # 搜索功能,根基你设定的类别取搜
    search_fields = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums']
    # 过滤器
    list_filter = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']

class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course__name','name','add_time']

class VideoAdmin(object):
    list_display = ['lesson','name','add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson','name','add_time']


class CourseResourceAdmin(object):
    list_display =  ['course', 'name', 'add_time', 'download']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'add_time', 'download']

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)

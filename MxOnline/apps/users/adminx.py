# _*_coding:utf-8_*_
import xadmin
from .models import *
from xadmin import views

#设置主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

#设置全局
class GlobalSetting(object):
    site_title = '无敌管理系统'
    site_footer = '无敌在线网'
    menu_style = 'accordion'

class EmailVarifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']

class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']


xadmin.site.register(EmailVarifyRecord,EmailVarifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)
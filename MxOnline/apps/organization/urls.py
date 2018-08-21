# _*_coding:utf-8_*_

from django.conf.urls import url,include
from .views import *

urlpatterns = [
                url(r'^list/$', OrgView.as_view(), name='org_list'),
                url(r'^add_mb/$',AddMbView.as_view(),name='add_mb'),
                                    # 下面正则表达式意义:捕获org_id并且匹配1到多个的数字,<id>会传到view视图,
                                    # 这里是为了匹配
                url(r'^coursedetail/(?P<id>\d+)/$',CourseOrgDetails.as_view(),name='courseorgdetail'),
                url(r'^coursedetail-c/(?P<org_id>\d+)/$',CourseDetails_c.as_view(),name='coursedetail-c'),
                url(r'^orgdesc/(?P<org_id>\d+)/$',OrgDesc.as_view(),name = 'orgdesc'),
                url(r'^orgteacher/(?P<id>\d+)/$',OrgTeacher.as_view(),name = 'orgteacher'),
                url(r'^addfav/$',AddFavView.as_view(),name='addfav'),
]

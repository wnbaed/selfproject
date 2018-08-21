# _*_coding:utf-8_*_

from django.conf.urls import url,include
from .views import *

urlpatterns = [
                url(r'^c-list/$', CourseList.as_view(), name='courselist'),
                url(r'^c-detail/(?P<course_id>\d+)/$',CourseDetail.as_view(),name='coursedetail'),
                url(r'^c-video/(?P<course_id>\d+)/$',CourseVideo.as_view(),name='coursevideo'),
                url(r'^c-comment/(?P<course_id>\d+)/$',CourseComment2.as_view(),name='coursecomment'),
                url(r'^c-add-comment/$',AddComment.as_view(),name='addcomment'),
                url(r'^video/(?P<video_id>\d+)/$',Video2.as_view(),name='video'),
]

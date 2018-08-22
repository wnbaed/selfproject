# _*_coding:utf-8_*_
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from .models import Course,Lesson,Video
from organization.models import CourseOrg
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite,CourseComment,UserCourse
from utils.mixin_untils import LoginRequiredMixin
# Create your views here.


class CourseList(View):
    def get(self,request):

        all_course = Course.objects.all()
        hot_course = all_course.order_by('-click_nums')[:5]
        # 按照最新,最热门,参与人数来排序,
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'new':
                all_course = all_course.order_by('-add_time')
            if sort == 'hot':
                all_course =  all_course.order_by('-click_nums')
            if sort == 'students':
                all_course = all_course.order_by('-students')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course,3)
        course = p.page(page)
        return render(request,'course-list.html',
                      {'all_course':course,
                       'hot_course':hot_course,
                       })


class CourseDetail(View):
    def get(self,request,course_id):
        coursedetail = Course.objects.get(id=int(course_id))
        coursedetail.click_nums += 1
        coursedetail.save()
        lesson = coursedetail.lesson_set.all()
        # 获取对应id的机构对象
        org = CourseOrg.objects.get(id = int(course_id))
        # 机构老师对象
        org_teacher = org.teacher_set.all()
        #机构教师数量
        org_teacher_num = org_teacher.count()
        # 课程标签，用于做相关推荐
        tag = coursedetail.tag
        if tag:
            # 这是要展示的对象，标签和浏览的课程相同的话就会被推荐，这个可以自己在后台定义
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            # 因为定了初始值是空，这里不设置空的就是空列表的话，html如果接收到空字符串，无法进行遍历
            relate_course = []
        # 课程收藏功能
        has_fav_c = False
        has_fav_o = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=coursedetail.id, fav_type=1):
                has_fav_c = True
            if UserFavorite.objects.filter(user=request.user, fav_id=coursedetail.courseorg.id, fav_type=2):
                has_fav_o = True
        return render(request,'course-detail.html',
                      {'course_detail':coursedetail,
                       'lesson':lesson,
                       'org':org,
                       'org_teacher_num':org_teacher_num,
                       'relate_course':relate_course,
                       'has_fav_c': has_fav_c,
                       'has_fav_o': has_fav_o,
                       })

# 具体课程章节视频详情
# @login_required
class CourseVideo(LoginRequiredMixin,View):
    def get(self,request,course_id):
        # 对应id课程的章节对象
        course_video = Course.objects.get(id=int(course_id))
        course_video.students += 1
        course_video.save()

        course_lesson = course_video.lesson_set.all()
        # 资源下载对象
        courseresource = course_video.courseresource_set.all()

        #查询用户是否关联了该课程
        user_course2 = UserCourse.objects.filter(user=request.user,course=course_video)
        if not user_course2:
            user_course3 = UserCourse(user=request.user,course=course_video)
            user_course3.save()
        # 筛选出用户的所有课程
        user_courses = UserCourse.objects.filter(course=course_video)
        # 用列表式取出遍历出所有学习用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        #获取所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course.id for all_user_course in all_user_courses]
        # 获取学过该用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        return render(request,'course-video.html',
                      {'course_video':course_video,
                       'course_lesson':course_lesson,
                       'courseresource':courseresource,
                       'relate_courses':relate_courses,
                       })

# 课程评论区1
class CourseComment2(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course_comment = Course.objects.get(id=int(course_id))
        courseresource = course_comment.courseresource_set.all()
        comments = course_comment.coursecomment_set.all()
        return render(request,'course-comment.html',
                      {'course_comment':course_comment,
                       'courseresource':courseresource,
                       'comments': comments,
                        })

# 添加评论功能1
class AddComment(View):
    def post(self,request):
        # 先监测是否登录
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status':'fail','msg':'用户未登录'}),content_type='application/json')

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')

        # 如果id和评论存在获取到了,把各项内容插入到数据库中
        if int(course_id) >0 and comments:
            course_comments = CourseComment()
            # 课程必须是对应id
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(json.dumps({'status':'success','msg':'发表评论成功'}),content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'fail','msg':'评论失败'}),content_type='application/json')


class Video2(View):
    # 视频播放页面
    def get(self, request, video_id):
        # 对应id课程的章节对象
        video = Video.objects.get(id=int(video_id))
        course_video = video.lesson.course
        course_video.students += 1
        course_video.save()

        course_lesson = course_video.lesson_set.all()
        # 资源下载对象
        courseresource = course_video.courseresource_set.all()

        # 查询用户是否关联了该课程
        user_course2 = UserCourse.objects.filter(user=request.user, course=course_video)
        if not user_course2:
            user_course3 = UserCourse(user=request.user, course=course_video)
            user_course3.save()
        # 筛选出用户的所有课程
        user_courses = UserCourse.objects.filter(course=course_video)
        # 用列表式取出遍历出所有学习用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course.id for all_user_course in all_user_courses]
        # 获取学过该用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-play.html',
                      {'course_video': course_video,
                       'course_lesson': course_lesson,
                       'courseresource': courseresource,
                       'relate_courses': relate_courses,
                       'video' : course_video,
                       'videoplay': video,
                       })



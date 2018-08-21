# _*_ coding:utf-8 _*_
import json

from django.shortcuts import render
from django.views.generic.base import View
from .models import *
# 下面两条都是分页功能的模块
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .form import UserAskForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from courses.models import Course
from operation.models import UserFavorite


# Create your views here.

#筛选分页函数
class OrgView(View):

    def get(self,request):
        #课程机构,all变量用于html遍历
        all_org = CourseOrg.objects.all()

        #热门机构提取
        hot_org = all_org.order_by('click')[:3]

        #城市
        all_city = CityDict.objects.all()

        # 取出筛选城市
        city_id = request.GET.get('city','')
        if city_id:
            #对all_org进一步筛选,让页面显示指定想要的
            all_org = all_org.filter(city_id=city_id)

        #筛选类别
        category = request.GET.get('ct','')
        if category:
            #对all_org进一步筛选,让页面显示指定想要的
            all_org = all_org.filter(category=category)

        # 按学生人数 或者 课程数来排序的逻辑
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students':
                #这里的all_org最终会传入下面的分页参数来继续运行
                all_org = all_org.order_by('-students')
            elif sort == 'courses':
                all_org = all_org.order_by('-course_nums')


        #课程总数
        all_num = all_org.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation
        #中间参数多少每页就显示多少个对象
        p = Paginator(all_org, 5 ,request=request)

        org = p.page(page)

        # if request.user.is_authenticated():

        return render(request,'org-list.html',{
            'all_org':org,
            'all_city':all_city,
            'all_num':all_num,
            'city_id':city_id,
            'category':category,
            'hot_org':hot_org,
            'sort' : sort,
            })
        # else:
        #     return render(request,'index.html')
#用户添加咨询
class AddMbView(View):
    # 此处和主要页面一起获取get请求,
    def post(self,request):
        # name1 = request.POST.get('name')
        # print(name1)
        user_askform = UserAskForm(request.POST)
        if user_askform.is_valid():
            #这里不写commit就不会做更改
            user_askform.save(commit=True)
            #运用json
            return HttpResponse(json.dumps({'status':'success'}),content_type='application/json')
        else:
            # return HttpResponse("{'status':'fail','msg':{0}}".format(user_askform.errors),content_type='json')
            return HttpResponse(json.dumps({'status':'fail','msg':'添加出错'}),content_type='application/json')
            # return HttpResponse("{'status':'fail','msg':'添加出错'}", content_type='application/json')

# 机构首页
class CourseOrgDetails(View):
    def get(self,request,id):
        current_page = 'home'
        #先获取课程机构的对应的id
        courseorg = CourseOrg.objects.get(id=int(id))
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=courseorg.id,fav_type=2):
                has_fav = True


        #再通过外键反向把Course里面的字段提取出来,机构和课程之间形成联动,对应的机构显示对应的课程
        all_course = courseorg.course_set.all()[:3]
        # 再通过外键反向把Teacher里面的字段提取出来,机构和课程之间形成联动,对应的机构显示对应的老师
        all_teacher = courseorg.teacher_set.all()[:2]
        return render(request,'org-detail-homepage.html',
                        {'all_course':all_course,
                         'all_teacher':all_teacher,
                         'course_org' : courseorg,
                         'current_page' : current_page,
                         'has_fav' : has_fav,
                         })

# 机构课程
class CourseDetails_c(View):
    def get(self,request,org_id):
        print(org_id)
        current_page = 'course'
        #先获取课程机构的对应的id
        courseorg = CourseOrg.objects.get(id=int(org_id))
        #再通过外键反向把Course里面的字段提取出来,机构和课程之间形成联动,对应的机构显示对应的课程
        all_course = courseorg.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=courseorg.id,fav_type=2):
                has_fav = True

        return render(request,'org-detail-course.html',
                        {'all_course':all_course,
                         'course_org' : courseorg,
                         'current_page' : current_page,
                         'has_fav': has_fav,
                         })

# 机构介绍
class OrgDesc(View):
    def get(self,request,org_id):
        current_page = 'desc'
        courseorg = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=courseorg.id):
                has_fav = True
        return render(request,'org-detail-desc.html',
                      {'course_org' : courseorg,
                       'current_page': current_page,
                       'has_fav' : has_fav,
                       })


# 机构讲师
class OrgTeacher(View):
    def get(self,request,id):
        current_page = 'teacher'
        courseorg = CourseOrg.objects.get(id=int(id))
        all_teacher = courseorg.teacher_set.all()[:2]
        #先设定是没收藏状态，如果登录了，再进行是否收藏的判断
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=courseorg.id,fav_type=2):
                has_fav = True
        return render(request,'org-detail-teachers.html',
                      {'course_org':courseorg,
                       'all_teacher':all_teacher,
                       'current_page':current_page,
                       'has_fav' : has_fav,
                       })

# 但凡有收藏的,都到此函数下运作,ajax用同一路径
class AddFavView(View):
    # 用户收藏,用户取消收藏
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return  HttpResponse(json.dumps({'status':'fail','msg':'用户未登录'}),content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_record:
            #如果记录已经存在,则表示用户取消收藏
            exist_record.delete()
            return HttpResponse(json.dumps({'status':'fail','msg':'收藏'}),content_type='application/json')
        else:
            # 如果不存在,则存储进数据库
            user_fav = UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                # model中的三个字段
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse(json.dumps({'status':'success','msg':'已收藏'}),content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status':'fail','msg':'收藏出错'}),content_type='application/json')




































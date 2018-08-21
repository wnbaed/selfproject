# _*_ encoding:utf-8 _*_
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVarifyRecord
from django.db.models import Q
#导入类View,定义后台逻辑用类来写
from django.views.generic.base import View
from .form import *
from django.contrib.auth.hashers import make_password
from utils.email_send import send_regsiter_email
from django.contrib.auth.decorators import login_required
# Create your views here.

#此处自定义 authenticate 的功能
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            #此处实现输入用户名或者邮箱,只要匹配都可以登录的逻辑
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#激活用户的代码
class ActiveUserView(View):
    # active_code 这里的值是点击了激活链接之后传进来的
    def get(self,request,active_code):
        #查询是否存在此邮箱是否存在
        all_records = EmailVarifyRecord.objects.filter(code=active_code)
        if all_records:
            for recored in all_records:
                email = recored.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            #跳转无效链接
            return render(request,'active_fail.html')
        return render(request,'login.html')



# def login_(request):
#     if request.method == 'POST':
#         user = Userinfo()
#         user.name = request.POST.get('username')
#         user.upassword = request.POST.get('pwd')
#         try:
#             find_user = Userinfo.objects.filter(uname = user.name)
#             if len(find_user) <= 0:
#                 messages.add_message(request, messages.ERROR, '该用户未注册')
#                 return redirect('user/login/')
#             if not check_password(user.upassword, find_user[0].upassword):
#                 return render(request, 'login.html',{'user_info': user, 'message_error': '用户名或密码错误'})
#         except ObjectDoesNotExist as e:
#             logging.warning(e)
#         request.session['user_id'] = find_user[0].id
#         request.session['user_name'] = find_user[0].uname
#         if request.COOKIES.get('url'):
#             url = request.COOKIES.get('url')
#             res = redirect(url)
#             res.delete_cookie('url')
#             return res
#         return redirect('/')
#     return redirect('/user/login')

class LoginView(View):
    def get(self,request):
        return render(request, 'login.html', {})
    def post(self,request):
        login_form = LoginForm(request.POST)
        #  .is_valid()判断是否满足表单的定义
        if login_form.is_valid():
            user_name = request.POST.get('username','')
            user_passwd = request.POST.get('password','')
            # find_user = UserProfile.objects.filter(username=user_name)
            user = authenticate(username=user_name,password=user_passwd)
            if user is not None:
                #判断是否已经通过邮箱激活
                if user.is_active:
                    login(request,user)

                    return render(request,'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活!'})
            else:
                return render(request, 'login.html', {'msg':'用户名或密码错误!'})

        else:
            #此处返回的表单的值是字典模式,可以在html遍历出错误提示
            # {% for key, error in login_form.errors.items %}{{error}}{% endfor %} {{msg}}
            return render(request, 'login.html', {'login_form':login_form})



class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})


    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email','')
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':'用户已经存在'})
            pass_word = request.POST.get('password','')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            #先默认注册时过后状态为未激活
            user_profile.is_active = False
            #将密码加密后再存入数据库
            user_profile.password = make_password(pass_word)
            user_profile.save()
            #发送注册邮件环节
            send_regsiter_email(user_name,'register')
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})



class ForgetPwdView(View):
    def get(self,request):
        #表单传入验证码功能
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        #判断表单是否合法
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            send_regsiter_email(email,'forget')
            #发送邮件成功返回成功页面
            return render(request,'send_success.html')
        else:
            return render(request,'active_fail.html')

#进入重置密码页面
class ResetView(View):
    def get(self, request,active_code):
        # 查询是否存在此邮箱是否存在
        all_records = EmailVarifyRecord.objects.filter(code=active_code)
        if all_records:
            for recored in all_records:
                email = recored.email
                #这里传回email值是为了知道到底是哪个用户修改密码,也能够让下面post函数可以通过
                #这个值来搜索比对email
                return render(request,'password_reset.html',{'email':email})

        else:
            # 跳转无效链接
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self,request):
        #参数一定要有request.POST
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            if password1 == password2:
                #这里要比对,来确认是要改的那个email用户对象
                user = UserProfile.objects.get(email=email)
                #别忘了重新改一次密码都要加密
                user.password = make_password(password1)
                user.save()
                return render(request,'login.html')
            else:
                return render(request,'password_reset.html',{'email':email,'msg':'两次密码不一致'})
        else:
            return render(request,'password_reset.html',{'modify_form':modify_form})


#退出登录
def login_out(request):
    logout(request)
    return redirect('/')



#   往后都使用基于类的方法写
# def login_(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username','')
#         user_passwd = request.POST.get('password','')
#         user = authenticate(username=user_name,password=user_passwd)
#         if user is not None:
#             login(request,user)
#
#             return render(request,'index.html')
#
#         else:
#             print('登录失败')
#             return render(request, 'login.html', {'msg':'用户名或密码错误!'})
#     elif request.method == 'GET':
#         return render(request,'login.html',{})



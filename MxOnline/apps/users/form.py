# _*_coding:utf-8_*_
from django import forms
#此处导入验证码模块
from captcha.fields import CaptchaField

#表单定义可以用于判断前端输入的值是否与这里设置的相符
class LoginForm(forms.Form):
    #变量名必须与html中name的名字一致
    username = forms.CharField(required=True)  #required=True 证明不能为空
    password = forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)
    #此处布置验证码表单
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    #此处布置验证码表单
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})

class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)



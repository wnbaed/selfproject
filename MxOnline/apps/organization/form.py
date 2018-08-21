# _*_coding:utf-8_*_
from django import forms
from operation.models import UserAsk
import re

#此处用的是ModelForm
class UserAskForm(forms.ModelForm):
    #功能强大,还可以新增字段
    # my_field = forms.CharField()
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']
    #重置手机号码要求,验证是否合法
    def clean_mobile(self):
        #从fields中取出来,初始化
        mobile = self.cleaned_data['mobile']
        #再用正则重定义
        REGEX_MOBILE = '1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法',code='mobile_invaild')


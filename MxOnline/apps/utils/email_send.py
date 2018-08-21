# _*_coding:utf-8_*_
from random import *
from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM

from users.models import EmailVarifyRecord

#随机生成字符串,当作激活链接里的字符串,下面写定的8后面赋值会覆盖掉
def ramdom_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMnOoPpQqRrSsTtUuVvXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str

#将此函数导入view视图,把从前端获取到的信息传入此函数,编好格式
# 最后发送邮件给setting设置好的邮箱
def send_regsiter_email(email,send_type='register'):
    email_record = EmailVarifyRecord()
    #生成16位长的字符
    code = ramdom_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    #保存到数据库
    email_record.save()

    email_title = ''
    email_body = ''


    if send_type == 'register':
        email_title = '无敌在线网激活注册连接'
        #在url多配置一个专门用于激活账号状态的路径,用format把之前编辑好的随机字符串传进地址
        #最后在view视图里做一个分析验证码的函数来分析,再给予激活
        email_body = '请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}'.format(code)
        #send_mail是一个功能函数,前两个参数分别是上面两个变量,第三个是setting里面定义的邮件来源
        #最后一个参数是前端传进来的用户账号(自己输进去的)
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    #覆盖原来传入的'register'
    elif send_type == 'forget':
        email_title = '无敌在线网密码链接'
        #在url多配置一个专门用于激活账号状态的路径,用format把之前编辑好的随机字符串传进地址
        #最后在view视图里做一个分析验证码的函数来分析,再给予激活
        email_body = '请点击下面的链接激活你的账号: http://127.0.0.1:8000/reset/{0}'.format(code)
        #send_mail是一个功能函数,前两个参数分别是上面两个变量,第三个是setting里面定义的邮件来源
        #最后一个参数是前端传进来的用户账号(自己输进去的)
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass







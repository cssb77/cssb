# !/usr/bin/python
# -*- coding: UTF-8 -*-
import ybc_box as q
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
www = q.enterbox('收件人邮箱账号')
if www == '':
            www ='yfgyfugyfy@163.com'
my_sender = 'yfgyfugyfy@163.com'  # 发件人邮箱账号
my_pass = 'zdlxwybfzgjgdjfj'  # 发件人邮箱密码
my_user = www  # 收件人邮箱账号，我这边发送给自己
wwww = q.ynbox('确认')
w = q.enterbox('主题')
ww = q.enterbox('填写邮件内容')
while wwww:
    def mail():
        ret = True
        try:
            global w,ww,www
            msg = MIMEText(ww, 'plain', 'utf-8')
            msg['From'] = formataddr(["FromRunoob", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] =w   # 邮件的主题，也可以说是标题

            #server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
             server = smtplib.SMTP_SSL("smtp.163.com", 25)
            server.login(my_sender, my_pass)  
            server.sendmail(my_sender, [my_user, ], msg.as_string()) 
            server.quit() 
        except Exception:  
            ret = False
        return ret
    ret = mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
def mail():
    ret = True
    try:
        global w,ww,www
        msg = MIMEText(ww, 'plain', 'utf-8')
        msg['From'] = formataddr(["66", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = w  # 邮件的主题，也可以说是标题j

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

ret = mail()
if ret:
    print("邮件发送成功")
else:
    print("邮件发送失败")
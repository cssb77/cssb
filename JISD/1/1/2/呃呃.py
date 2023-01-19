import  smtplib
from    email.mime.text import MIMEText #
print("1")
print("邮件发送成功")

SMTPsever="smtp.163.com"
Sender="yfgyfugyfy@163.com"
password="CJKAWZRNQFLAKAGQ"
print("2")

Message="hello"
msg=MIMEText(Message)
print("3")

msg["Subject"]='hhhhhh'
msg["From"]=Sender
msg["To"]="a715548679@163.com"
print("4")

mailsever=smtplib.SMTP(SMTPsever,25)
mailsever.login(Sender,password)
mailsever.sendmail(Sender,["2506325721@163.com","yfgyfugyfy@163.com"],msg=as_string())
mailsever.quit()
print("over")
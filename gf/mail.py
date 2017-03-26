# encoding: UTF-8
import smtplib
import json
import sys
from datetime import *

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

def send_email(user='allenwwg', pwd='this1@dog', recipient='wenguang.wang@intergraph.com', subject='mail test', body=''):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    #message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    #""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    msg = MIMEMultipart('alternative')
    msg.set_charset('utf8')
    msg['FROM'] = FROM
    bodyStr = body

    #This solved the problem with the encode on the subject.
    msg['Subject'] = Header(
        subject.encode('utf-8'),
        'UTF-8'
    ).encode()
    msg['To'] = recipient
    # And this on the body
    _attach = MIMEText(bodyStr.encode('utf-8'), 'html', 'UTF-8')        
    msg.attach(_attach) 
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print('successfully sent the mail')
    except Exception as e:
        print(e)
def send_163_email(subject,message):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    '''
    记得请先开启邮箱的SMTP服务
    '''
    ## 发送邮件
    sender = 'allenwwg@163.com' #发送的邮箱
    receiver = 'wenguang.wang@intergraph.com' #要接受的邮箱（注:测试中发送其他邮箱会提示错误）
    smtpserver = 'smtp.163.com' 
    username = 'allenwwg@163.com' #你的邮箱账号
    password = '36740s' #你的邮箱密码

    msg = MIMEText(str(message),'plain','utf-8') #中文需参数‘utf-8'，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8') #邮件主题
    msg['to'] = receiver      
    msg['from'] = sender    #自己的邮件地址 

    smtp = smtplib.SMTP()
    try :
        smtp.connect('smtp.163.com') # 链接
        smtp.login(username, password) # 登陆
        smtp.sendmail(sender, receiver, msg.as_string()) #发送
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败')
        print(e)
    smtp.quit() # 结束
	
def send_qq_email(subject,message):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    ## 发送邮件
    sender = 'allenwwg@qq.com' #发送的邮箱
    receiver = 'wenguang.wang@intergraph.com' #要接受的邮箱（注:测试中发送其他邮箱会提示错误）
    smtpserver = 'smtp.qq.com' 
    username = 'allenwwg@qq.com' #你的邮箱账号
    password = 'gtpkcgbrnplibjcf' #你的邮箱授权码。一个16位字符串

    msg = MIMEText(str(message),'plain','utf-8') #中文需参数‘utf-8'，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8') #邮件主题
    msg['to'] = receiver      
    msg['from'] = sender    #自己的邮件地址 

    server = smtplib.SMTP_SSL('smtp.qq.com')
    try :
        #server.connect() # ssl无需这条
        server.login(username, password) # 登陆
        server.sendmail(sender, receiver, msg.as_string()) #发送
        print('邮件发送成功')
    except:
        print('邮件发送失败')
    server.quit() # 结束

if __name__ == '__main__':
    #send_email(subject=u'Get EventLog__:2016-11-09 14:50:49:今日总成交合约数量10，超过限制10')
	#send_qq_email(subject='Info from JoinQuant', message="test mail")
	send_163_email(subject='Info from JoinQuant', message="test mail")

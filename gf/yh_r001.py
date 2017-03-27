# encoding: UTF-8
import urllib.request

requrl = 'http://allenwwg.cn/bR01/taurus'
msg = requests.get(requrl)
print(msg)

send_email(subject = msg,body = '')

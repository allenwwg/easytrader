# coding: utf-8
import urllib.request

requrl = 'allenwwg.cn'
#req = urllib.request.Request('baidu.com',"")
response = urllib.request.urlopen('http://allenwwg.cn/buy/600166/100/8.3')
print(response.read())
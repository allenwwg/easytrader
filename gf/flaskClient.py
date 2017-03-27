# coding: utf-8


#import urllib.request #2.7
import requests, json

requrl = 'http://allenwwg.cn/'
#req = urllib.request.Request('baidu.com',"")
#response = urllib.request.urlopen('http://allenwwg.cn/balance')
#print(response.read())
r = requests.get(requrl + 'balance')
print(r.text)

r = requests.get(requrl + 'ipo/today')
print(r.text)
# encoding: UTF-8

import smtplib

import easytrader
import json
import logging
from datetime import *
from mail import *
from logger import *

user = easytrader.use('yh',debug=False)
user.prepare('u:\yh.json')
msg =  str(user.balance) + ', ' + datetime.now().date().isoformat()

#print user balance
print(msg)

#write a log to file test.log
fire_log(msg)

#get ipo information
ipoInfo = user.get_ipo_info()
print(str(ipoInfo))
fire_log(str(ipoInfo)+'\n')

debug_info=''
today_ipo = str(ipoInfo[0])

if len(today_ipo):
	ipo_arr = today_ipo.split('\n')
	arr_len = len(ipo_arr)

	for index in range(arr_len):
		if index==0:
		   continue
		ipoInfo = ipo_arr[index]
		ipo = ipoInfo.split('  ')
		if(len(ipo)>5 and ipo[4]!=''):
			r1 = user.buy(ipo[1],float(ipo[3]),int(ipo[4]))
			debug_info = debug_info+'\n'+str(r1)
			
print(debug_info)
fire_log(debug_info+'\n')
   
user.exit()
send_email(subject = msg,body = debug_info)

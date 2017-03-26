# encoding: UTF-8

import easytrader
from mail import *

user = easytrader.use('yh',debug=False)
user.prepare('c:\yh.json')
aviliable_money = user.balance[0]['可用资金']

msg = ''
if aviliable_money > 1000:
	sell_amount = int(aviliable_money / 1000)*10
	result = user.sell('131810',1.0, sell_amount);
	msg = str(result)
	print(msg)
else :
	msg = 'No enough money for r-001'
	print (msg)
   
user.exit()
send_email(subject = msg,body = '')

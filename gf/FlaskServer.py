# encoding: UTF-8
import atexit
from flask import Flask
import easytrader
from easytrader import helpers
import json
from logger import *
#from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
#from flask_apscheduler import utils
import time
from datetime import *	 
#import aiohttp
#import asyncio

from gevent import monkey
from gevent.pywsgi import WSGIServer

from mail import *

monkey.patch_all()

app = Flask(__name__)
app.config.update(DEBUG=False)

global g_user,g_securityID
g_user = ''
g_securityID = 'taurus'

def init0():
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
	inited = True
	
	try:
		global g_user
		#if g_user == '':
		g_user = easytrader.use('yh',debug=False)
		g_user.prepare('u:\yh.json')
		#print(str(inited) + ': YinHe config initialized')
	except Exception as e:
		print(e)
		inited = False
	msg0 = '{0}: YinHe config initialized @ {1}'	
	msg0 = msg0.format(str(inited), dateTime())
	print(msg0)
	
	sendMsg(msg=msg0, securityID = g_securityID)
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
	return msg0
	
@app.route('/i/<securityID>')
@app.route('/init/<securityID>')
def init(securityID):
	rst = 'False'
	if securityID != str(g_securityID):
		return rst
	return init0()	

@app.route('/')
def root():
	rst = 'Fighting, 18516391949'
	return rst
	
@app.route('/h')
@app.route('/help')
def help():
	rst = '/help </br> \
			/balance </br> \
			/position </br> \
			/entrust/today </br> \
			/deal/today </br> \
			/ipo/today </br> \
			/buy/stockID/price/amount/securityID </br> \
			/sell/stockID/price/amount/securityID </br> \
			'
	return rst
	
@app.route('/s')
@app.route('/servers')
def servers():
	rst = 'aws linux -> 52.79.43.219 </br> \
			aws windows -> 13.124.41.247 </br> \
			'
	return rst
	
@app.route('/b')
@app.route('/balance')
def balance():
	rst = 'False'
	try:
		rst = str(g_user.balance)
	except Exception as e:
		return rst
	return rst.replace(',','</br>')	

@app.route('/it')
@app.route('/ipo/today')
def ipoToday():
	rst = 'False'
	try:
		rst = str(g_user.get_ipo_info())
	except Exception as e:
		return rst
	return rst	
	
@app.route('/et')
@app.route('/entrust/today')
def entrust():
	rst = 'False'
	try:
		rst = str(g_user.entrust)
	except Exception as e:
		return rst
	return rst.replace('}, {','</br>')	
	
@app.route('/dt')
@app.route('/deal/today')
def dealToday():
	rst = 'False'
	try:
		rst = str(g_user.current_deal)
	except Exception as e:
		return rst
	return rst.replace('}, {','</br>')	
	
@app.route('/p')
@app.route('/position')
def position():
	rst = 'False'
	try:
		rst = str(g_user.position)
	except Exception as e:
		return rst
	return rst.replace('}, {','</br>')	
	
@app.route('/sm/<msg>/<securityID>')	
@app.route('/sendmsg/<msg>/<securityID>')
def sendMsg(msg,securityID):
	rst = 'False'
	if securityID != str(g_securityID):
		return rst
	try:
		send_139_email(subject=str(msg), message='')
		rst = 'True'
	except Exception as e:
		pass
	return rst
	
@app.route('/br01/<securityID>')
@app.route('/buyR01/<securityID>')
def buyR01(securityID):
	rst = 'False'
	if securityID != str(g_securityID):
		return rst

	try:
		aviliable_money = g_user.balance[0]['可用资金']
		if aviliable_money > 1000:
			sell_amount = int(aviliable_money / 1000)*10
			result = g_user.sell('131810',1.0, sell_amount);
			rst = 'True:' + ' ' + str(result)
			print(rst)
		else:
			rst = 'False:' + ' ' + 'No enough money for r-001'
			print (rst)
	except Exception as e:
		pass
	#sendMsg(msg=str(rst), securityID = g_securityID)
	return rst
	
@app.route('/ai/<securityID>')
@app.route('/autoIpo/<securityID>')
def autoYhIpo(securityID):
	rst = 'False'
	if securityID != str(g_securityID):
		return rst

	try:
		#get ipo information
		ipoInfo = g_user.get_ipo_info()
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
					print('{0},{1},{2}\n'.format(ipo[1],ipo[3],ipo[4]))
					r1 = g_user.buy(stock_code = ipo[1],price = float(ipo[3]),amount = int(ipo[4]))
					debug_info = debug_info+'\n'+str(r1)
					rst = 'True'
		if debug_info == '':
			debug_info = "No IPO Today"
		print(debug_info)
		fire_log(debug_info+'\n')
		rst = rst + ": " + debug_info
	except Exception as e:
		rst = str(e)
	
	#sendMsg(msg=str(rst), securityID = g_securityID)
	
	return rst

@app.route('/gfIpo/<securityID>')
def autoGfIpo(securityID):	
	user = easytrader.use('gf',debug=False)
	user.prepare('u:\gf.json')
	marketValue = user.balance['data'][0]['market_value']
	enableBalance = user.balance['data'][0]['enable_balance']
	total = float(marketValue) + float(enableBalance)
	msg = 'gf, '+ marketValue +', '+ enableBalance + ', ' + str(total) + ', ' + datetime.now().date().isoformat()
	ipo_data = helpers.get_today_ipo_data()
	ipo_limit = user.today_ipo_limit()
	Dic_amount = {'上海':0.0,'深圳':0.0}
	for limit in ipo_limit['data']:
		Dic_amount[limit['exchange_type_dict']] = float(limit['enable_amount'])
		
	for data in ipo_data:
		apply_code = data['apply_code']
		price = data['price']
		stock_code = data['stock_code']
		amount = 0
		if 'SZ' in stock_code:
			amount = Dic_amount['深圳']
		if 'SH' in stock_code:
			amount = Dic_amount['上海']
		if amount > 0:
			user.buy(apply_code,float(price),amount)
		
	user.exit()
@app.route('/b/<stockID>/<price>/<amount>/<securityID>')
@app.route('/buy/<stockID>/<price>/<amount>/<securityID>')
def buy(stockID, price, amount, securityID):
	rst = 'False'
	if securityID != str(g_securityID):
		return rst

	try:
		print(str(stockID))
		print(str(price))
		print(str(amount))
		rst = g_user.buy(str(stockID),float(price),int(amount))
		return str(rst)
	except Exception as e:
		return rst
	return rst
	
@app.route('/s/<stockID>/<price>/<amount>/<securityID>')
@app.route('/sell/<stockID>/<price>/<amount>/<securityID>')
def sell(stockID, price, amount, securityID):
	rst = 'False'
	if securityID != str(g_securityID):
		return rst
	try:
		print(str(stockID))
		print(str(price))
		print(str(amount))
		rst = g_user.sell(str(stockID),float(price),int(amount))
		return str(rst)
	except Exception as e:
		return rst
	return rst

@app.route('/datetime')
def dateTime():
	return '{0} {1}'.format(datetime.now().date().isoformat(), datetime.now().time().isoformat())

@app.route('/dr')
@app.route('/dor01')
def doR01():
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
	print('Doing R01 job @ {0}\n'.format(dateTime()))
	rst = buyR01(str(g_securityID))
	doneMsg = '{0}: Done R01 job @ {1}\n'.format(rst,dateTime())
	print(doneMsg)
	sendMsg(msg=doneMsg, securityID = g_securityID)
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
	return doneMsg
@app.route('/di')	
@app.route('/doipo')	
def doIpo():
	doneMsg = ''
	try:
		print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
		print('Doing YinHe Ipo job @ {0}.....\n'.format(dateTime()))
		rst = autoYhIpo(str(g_securityID))
		doneMsgYh = '{0}\n: Done YinHe Ipo job @ {1}.....\n'.format(rst, dateTime())
		print(doneMsgYh)
		
		print('Doing GuangFa Ipo job @ {0}.....\n'.format(dateTime()))
		rst = autoGfIpo(str(g_securityID))
		doneMsgGf = '{0}\n: Done GuangFa Ipo job @ {1}.....\n'.format(rst, dateTime())
		print(doneMsgGf)
		
		doneMsg = doneMsgYh + '\n' + doneMsgGf
		sendMsg(msg=doneMsg, securityID = g_securityID)
		print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
	except Exception as e:
		doneMsg = str(e)
	return doneMsg.replace('\n','</br>')

def balanceReport():
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
	print('Sending balance job @ {0}.....\n'.format(dateTime()))
	rst = sendMsg(balance(),g_securityID)
	doneMsgGf = '{0}\n: Done sending balance job @ {1}.....\n'.format(rst, dateTime())
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')

class Config(object):
    JOBS = [
        {
            'id': 'InitJob1',
            'func': 'FlaskServer:init0',
            'trigger': {
				'type': 'cron',
				'minute': 1,
				'hour': 9,
				'day_of_week' : '0-4',
				'misfire_grace_time' : 90
            }
        },
		{
            'id': 'InitJob2',
            'func': 'FlaskServer:init0',
            'trigger': {
				'type': 'cron',
				'minute': 50,
				'hour': 12,
				'day_of_week' : '0-4',
				'misfire_grace_time' : 90
            }
        },
		{
            'id': 'IpoJob',
            'func': 'FlaskServer:doIpo',
            'trigger': {
				'type': 'cron',
				'minute': 35,
				'hour': 9,
				'day_of_week' : '0-4',
				'misfire_grace_time' : 90
            }
        },
		{
            'id': 'R01Job',
            'func': 'FlaskServer:doR01',
            'trigger': {
				'type': 'cron',
				'minute': 50,
				'hour': 14,
				'day_of_week' : '0-4',
				'misfire_grace_time' : 90
            }
        },
		{
            'id': 'BalanceJob',
            'func': 'FlaskServer:balanceReport',
            'trigger': {
				'type': 'cron',
				'minute': 1,
				'hour': 15,
				'day_of_week' : '0-4',
				'misfire_grace_time' : 90
            }
        },
		{
            'id': 'helloJob',
            'func': 'FlaskServer:hello',
            'trigger': {
				'type': 'cron',
				'minute': 53,
				'hour': 9,
				'day_of_week' : '0-4',
				'misfire_grace_time' : 90
            }
        }
    ]

	
def initSchedule():
	app.config.from_object(Config())
	scheduler = APScheduler()
	scheduler.init_app(app)
	scheduler.start()
	print("Scheduler Initialized\n")

@app.route('/hello')
def hello():
	print('hello')
	return 'hello'

@app.route('/asyn')
def test_asyn_one():
    asyncTest()
    return 'true'

def asyncTest():
	time.sleep(15)
	print('hello asyn')


if __name__ == '__main__':
	
	init0()
	initSchedule()
	app.run(host='localhost', port=80,threaded=True,debug=True)
	#http_server = WSGIServer(('', 80), app)
	#http_server.serve_forever()
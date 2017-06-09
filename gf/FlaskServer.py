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
from time import sleep
from datetime import *	 
#import aiohttp
#import asyncio

from gevent import monkey
from gevent.pywsgi import WSGIServer

from mail import *

monkey.patch_all()

app = Flask(__name__)
app.config.update(DEBUG=False)

#yinhe config
global g_yhUser, g_gfUser, g_securityID
g_yhUser = ''
g_gfUser = ''
g_securityID = 'taurus'

def init0(broker = 'yh'):
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
	inited = True
	
	try:
		global g_yhUser, g_gfUser
		if broker == 'yh':
			g_yhUser = easytrader.use('yh',debug=False)
			g_yhUser.prepare('u:\yh.json')
		
		if broker == 'gf':
			g_gfUser = easytrader.use('gf',debug=False)
			g_gfUser.prepare('u:\gf.json')
		
		#print(str(inited) + ': YinHe config initialized')
	except Exception as e:
		print(e)
		inited = False
	msg0 = '{0}: config initialized @ {1}'	
	msg0 = msg0.format(str(inited), dateTime())
	print(msg0)
	
	_sendMsg(msg=msg0)
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
	return msg0
	
@app.route('/i/<broker>/<securityID>')
@app.route('/init/<broker>/<securityID>')
def init(broker, securityID):
	rst = 'False'
	if securityID != str(g_securityID):
		return rst
	return init0(broker)	

@app.route('/')
def root():
	rst = 'Fighting, 18516391949, 18521007606'
	return rst
	
@app.route('/h')
@app.route('/help')
def help():
	rst = 'help -> /help </br> \
			balance -> /balance </br> \
			position -> /position </br> \
			today entrust -> /entrust/today </br> \
			today deal -> /deal/today </br> \
			today ipo -> /ipo/today </br> \
			buy -> /buy/stockID/price/amount/securityID </br> \
			sell -> /sell/stockID/price/amount/securityID </br> \
			auto Yh IPO -> /ai/securityID </br> \
			auto GF IPO -> /gi/securityID </br> \
			send message -> /sm/msg/securityID </br> \
			servers -> /servers </br> \
			'
	return rst
	
@app.route('/s')
@app.route('/servers')
def servers():
	rst = 'aws linux -> 52.79.43.219 </br> \
			aws windows -> 13.124.41.247 </br> \
			'
	return rst
	
@app.route('/b/<broker>')
@app.route('/balance/<broker>')
def balance(broker):
	CheckLogin(broker)
	rst = 'False'
	try:
		if broker == 'yh':
			rst = str(g_yhUser.balance)
		if broker == 'gf':
			rst = str(g_gfUser.balance)
	except Exception as e:
		return rst
	return rst.replace(',','</br>')	

@app.route('/it/<broker>')
@app.route('/ipo/today<broker>')
def ipoToday(broker):
	CheckLogin(broker)
	rst = 'False'
	try:
		if broker == 'yh':
			rst = str(g_yhUser.get_ipo_info())
		if broker == 'gf':
			rst =  str(g_gfUser.today_ipo_limit())

	except Exception as e:
		return rst
	return rst	
	
@app.route('/et/<broker>')
@app.route('/entrust/today/<broker>')
def entrust(broker = 'yh'):
	CheckLogin(broker)
	rst = 'False'
	try:
		if broker == 'yh':
			rst = str(g_yhUser.entrust)
		if broker == 'gf':
			rst = str(g_gfUser.entrust)
			
	except Exception as e:
		return rst
	return rst.replace('}, {','</br>')	
	
@app.route('/dt/<broker>')
@app.route('/deal/today/<broker>')
def dealToday(broker = 'yh'):
	CheckLogin()
	rst = 'False'
	try:
		if broker == 'yh':
			rst = str(g_yhUser.current_deal)
		if broker == 'gf':
			rst = str(g_gfUser.current_deal)
	except Exception as e:
		return rst
	return rst.replace('}, {','</br>')	
	
@app.route('/p/<broker>')
@app.route('/position/<broker>')
def position(broker = 'yh'):
	rst = 'False'
	try:
		if broker == 'yh':
			rst = str(g_yhUser.position)
		if broker == 'gf':
			rst = str(g_gfUser.position['data'])
	except Exception as e:
		return rst
	return rst.replace('}, {','</br>')	

@app.route('/hl/<broker>')
@app.route('/holdlist/<broker>')
def holdingList(broker = 'yh'):
	CheckLogin(broker)
	codes = []
	try:
		if broker == 'yh':
			positions = g_yhUser.position
			for p in positions:
				ext = '.XSHG'
				if p['交易市场'] == '深A':
					ext = '.XSHE'
				code = p['证券代码'] + ext
				codes.append(code)
		if broker == 'gf':
			positions = g_gfUser.position['data']
			for p in positions:
				ext = '.XSHG'
				if p['exchange_type_dict'] != '上海':
					ext = '.XSHE'
				code = p['stock_code'] + ext
				codes.append(code)
			
	except Exception as e:
		return False
	return json.dumps(codes)


def _sendMsg(msg):
	rst = 'False'
	try:
		send_139_email(subject=str(msg),  message='')
		rst = 'True'
	except Exception as e:
		pass
	return rst
	
@app.route('/sm/<msg>/<tolist>/<securityID>')	
@app.route('/sendmsg/<msg>/<tolist>/<securityID>')
def sendMsgTo(msg, tolist, securityID='taurus'):
	rst = 'False'
	if securityID != str(g_securityID):
		return rst
	try:
		#gigiEmail = '15900443703@139.com'
		print(tolist)
		send_139_email(subject=str(msg),  message='', to = str(tolist))
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
		aviliable_money = g_yhUser.balance[0]['可用资金']
		if aviliable_money > 1000:
			sell_amount = int(aviliable_money / 1000)*10
			result = g_yhUser.sell('131810',1.0, sell_amount);
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
		ipoInfo = g_yhUser.get_ipo_info()
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
					r1 = g_yhUser.buy(stock_code = ipo[1],price = float(ipo[3]),amount = int(ipo[4]))
					sleep(0.5)
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
	
def _sleep(sec):
	sleep(sec)

@app.route('/gi/<securityID>')
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
		
	rst = '';
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
			e = user.buy(apply_code,float(price),amount)
			rst = rst + str(e)
			sleep(0.5)
		
	user.exit()
	return rst

@app.route('/b/<broker>/<stockID>/<price>/<amount>/<securityID>')
@app.route('/buy/<broker>/<stockID>/<price>/<amount>/<securityID>')
def buy(broker, stockID, price, amount, securityID):
	CheckLogin(broker)
	rst = 'False'
	if securityID != str(g_securityID):
		return rst

	try:
		print(str(stockID))
		print(str(price))
		print(str(amount))
		if broker == 'yh':
			rst = g_yhUser.buy(str(stockID),float(price),int(amount))
		if broker == 'gf':
			rst = g_gfUser.buy(str(stockID),float(price),int(amount))
		_sleep(0.5)
		return str(rst)
	except Exception as e:
		return rst

	return rst
	
@app.route('/s/<broker>/<stockID>/<price>/<amount>/<securityID>')
@app.route('/sell/<broker>/<stockID>/<price>/<amount>/<securityID>')
def sell(broker, stockID, price, amount, securityID):
	CheckLogin(broker)
	if _positionExists(broker, stockID) == False:
		return 'Not existing position for ' + stockID
	rst = 'False'
	if securityID != str(g_securityID):
		return rst
	try:
		print(str(stockID))
		print(str(price))
		print(str(amount))
		if(int(amount) == 0):
			amount = _getPositionAmount(broker,stockID)
		if broker == 'yh':
			rst = g_yhUser.sell(str(stockID),float(price),int(amount))
		if broker == 'gf':
			rst = g_gfUser.sell(str(stockID),float(price),int(amount))
		_sleep(0.5)
		return str(rst)
	except Exception as e:
		return rst
	return rst
	
def _positionExists(broker,stockID):
	return stockID in str(holdingList(broker))

@app.route('/amount/<broker>/<stockID>')
def getStockAviliableAmout(broker,stockID):
	return str(_getPositionAmount(broker, stockID))

def _getPositionAmount(broker, stockID):
	amount = 0
	try:
		if broker == 'yh':
			positions = g_yhUser.position
			for p in positions:
				if p['证券代码'] == stockID:
					amount = int(p['股份可用'])
					break
		if broker == 'gf':
			positions = g_gfUser.position['data']
			for p in positions:
				if p['stock_code'] == stockID:
					amount = int(p['enable_amount'])
					break

	except Exception as e:
		return 0
	
	return amount
	
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

def CheckLogin(broker = 'yh'):
	if isLogin(broker) == False:
		init0(broker)
	
def isLogin(broker = 'yh'):
	rst = position(broker)
	if rst == 'False':
		return False
	return True

class Config(object):
    JOBS = [
        {
            'id': 'InitJob1',
            'func': 'FlaskServer:init0',
            'trigger': {
				'type': 'cron',
				'minute': 14,
				'hour': 9,
				'day_of_week' : '0-4',
				'misfire_grace_time' : 10
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
				'misfire_grace_time' : 10
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
				'misfire_grace_time' : 10
            }
        },
		{
            'id': 'R01Job',
            'func': 'FlaskServer:doR01',
            'trigger': {
				'type': 'cron',
				'minute': 51,
				'hour': 14,
				'day_of_week' : '0-4',
				'misfire_grace_time' : 10
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
				'misfire_grace_time' : 10
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
	time.sleep(1)
	print('hello asyn')


if __name__ == '__main__':
	
	init0('yh')
	init0('gf')
	initSchedule()
	app.run(host='0.0.0.0', port=80,threaded=True,debug=True)
	#http_server = WSGIServer(('', 80), app)
	#http_server.serve_forever()
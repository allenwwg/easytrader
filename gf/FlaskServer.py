from flask import Flask
import easytrader
import json

import aiohttp
import asyncio

from gevent import monkey
from gevent.pywsgi import WSGIServer

from mail import *

monkey.patch_all()

app = Flask(__name__)
app.config.update(DEBUG=True)

global g_user,g_securityID
g_user = ''
g_securityID = ''

def init0():
	inited = True
	try:
		global g_user
		#if g_user == '':
		g_user = easytrader.use('yh',debug=False)
		g_user.prepare('u:\yh.json')
		print('YinHe config initialized')
	except Exception as e:
		print(e)
		inited = False
	return str(inited)
	
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
	return rst

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
	return rst
	
@app.route('/dt')
@app.route('/deal/today')
def dealToday():
	rst = 'False'
	try:
		rst = str(g_user.current_deal)
	except Exception as e:
		return rst
	return rst	
	
@app.route('/p')
@app.route('/position')
def position():
	rst = 'False'
	try:
		rst = str(g_user.position)
	except Exception as e:
		return rst
	return rst
	
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
	
@app.route('/bR01/<securityID>')
@app.route('/buyR01/<securityID>')
def buyR01(securityID):
	rst = 'False'
	if securityID != str(g_securityID):
		return rst

	try:
		aviliable_money = user.balance[0]['可用资金']
		if aviliable_money > 1000:
			sell_amount = int(aviliable_money / 1000)*10
			result = g_user.sell('131810',1.0, sell_amount);
			rst = str(result)
			print(rst)
		else:
			rst = 'No enough money for r-001'
			print (rst)
		return str(rst)
	except Exception as e:
		pass
	return rst
	
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
	
@app.route('/hello')
def hello():
	return 'hello'

import time	
@app.route('/asyn')
def test_asyn_one():
    asyncTest()
    return 'true'

def asyncTest():
	time.sleep(15)
	print('hello asyn')
if __name__ == '__main__':
	init0()
	app.run(host='0.0.0.0', port=80,threaded=True,debug=True)
	#http_server = WSGIServer(('', 80), app)
	#http_server.serve_forever()

import smtplib
import easytrader
import json
from datetime import *
from easytrader import helpers

def send_email(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")

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
#print(user.balance)
#print(msg)

f = open('log.txt','a')
f.write(msg+'\n')
f.close()

send_email('allenwwg','this1@dog','wenguang.wang@intergraph.com',msg, '')



import easytrader
import json
user = easytrader.use('yh',debug=False)
user.prepare('u:\yh.json')print(str(user.balance))

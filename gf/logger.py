# encoding: UTF-8
import logging

def fire_log(msg):
    logging.basicConfig(level=logging.DEBUG,  
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s \n %(message)s',  
                        datefmt='%a, %d %b %Y %H:%M:%S',  
                        filename='u:/python3.5/gf/test.log',  
                        filemode='a')  
    logging.info(msg)
if __name__ == '__main__':
    fire_log(msg=u'Get EventLog__:2016-11-09 14:50:49:今日总成交合约数量10，超过限制10')
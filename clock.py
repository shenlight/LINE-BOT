from apscheduler.schedulers.blocking import BlockingScheduler
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from dbModel import Order,OrderDetail
from dbAdd import TimeCheck,read

line_bot_api = LineBotApi('N97P2OvLyWzhxJHNQgLpCUymUSkNMdiSQBqKgaOXBU5AAVOMuTNbA1whs1Ocy4Ozk2hsFoUbvn+KicYgFT24DKdArnej2tne/q31PvbeahGjKcnIMuBkOECg2Df6TXMbBvupbgxTnAXqDcpyKgylSgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('38d5c2f5185a44fa17ffe21e3788ccc2')

sched = BlockingScheduler()
@sched.scheduled_job('interval',minutes=1)
def time_job():
    getresult = TimeCheck()
    print(getresult)
    if(getresult!=[]):
        for x in getresult:
            r = read(x)
            print(r)
            if(r=="查無資料"):
                pass
            else: 
                readresult = "OrderID:"+r[0]+"\n地區:"+r[1]+"\n外送者:"+r[2]+"\n使用者:"+r[3]+"\n收單時間:"+r[4]+"\n送達時間:"+r[5]+"\n上限份數:"+r[6]+"\n訂單明細:"+r[7]+"\n目前總份數:"+r[8]
                line_bot_api.push_message("U879fdf1cc34bb4c11099be8ffb9b6bb8",TextSendMessage(text=readresult))
sched.start()

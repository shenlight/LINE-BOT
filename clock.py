from apscheduler.schedulers.blocking import BlockingScheduler
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime,timedelta
from funtion import TimeCheck,Timedelete

line_bot_api = LineBotApi('')
handler = WebhookHandler('')

#TODO read 方法要修改 此為用ID查詢訂單方法
sched = BlockingScheduler()
@sched.scheduled_job('interval',minutes=1)
def time_job():
    r = TimeCheck()
    
    if(r!="查無資料"):
        for x in range(0,len(r),10):
            readresult = "訂單成立\nOrderID:"+r[x]+"\n地區:"+r[x+1]+"\n外送者:"+r[x+2]+"\n使用者:"+r[x+3]+"\n收單時間:"+r[x+4]+"\n送達時間:"+r[x+5]+"\n上限份數:"+r[x+6]+"\n訂單明細:"+r[x+7]+"\n目前總份數:"+r[x+8]+"\n取貨地點:"+r[x+9]
            line_bot_api.push_message("U879fdf1cc34bb4c11099be8ffb9b6bb8",TextSendMessage(text=readresult))
    else:
        pass
    Timedelete()
sched.start()

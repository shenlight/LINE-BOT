# encoding: utf-8
from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi,WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import TemplateSendMessage,ButtonsTemplate,PostbackAction,PostbackEvent
from datetime import datetime,timedelta
import re

from dbAdd import Delivery_add,User_add,UserInputCheck,UserUpdates,read,readall,deleteOrder

line_bot_api = LineBotApi('N97P2OvLyWzhxJHNQgLpCUymUSkNMdiSQBqKgaOXBU5AAVOMuTNbA1whs1Ocy4Ozk2hsFoUbvn+KicYgFT24DKdArnej2tne/q31PvbeahGjKcnIMuBkOECg2Df6TXMbBvupbgxTnAXqDcpyKgylSgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('38d5c2f5185a44fa17ffe21e3788ccc2')


app = Flask(__name__)
#Cd495babd31cff04b3743958031d8dd71
# 設定你接收訊息的網址，如 https://YOURAPP.herokuapp.com/callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    #uID = event.source.user_id
    content = event.message.text
    
    if content =="功能":
        menu(event)
    
    elif content.find("查詢全部")!=-1:
        searchall(event)

    elif content.find("外送者")!=-1:
        delivery_input(event)

    elif content.find("使用者")!=-1:
        user_input(event)

    elif content.find("刪除訂單編號")!=-1:
        delete(event)
    
    else:
        pass


@handler.add(PostbackEvent)
def handle_postback(event):

    if event.postback.data == 'delivery_ex':
        delivery_ex(event)

    elif event.postback.data == 'user_ex':
        user_ex(event)

    elif event.postback.data == 'search':
        search(event)

    elif event.postback.data == 'delete_ex':
        delete_ex(event)
    
def menu(event):
    buttons_template = ButtonsTemplate(title='全全外送很高興為您服務',text='請點選要使用的功能並依照指示操作\n目前僅開放司機發起訂單，使用者跟隨的服務模式',actions=[
        PostbackAction(label='可順路幫外送(司機)',text=None,data='delivery_ex'),
        PostbackAction(label='需要幫外送(使用者)',text=None,data='user_ex'),
        PostbackAction(label='查詢自己的訂單',text=None,data='search'),
        PostbackAction(label='刪除訂單',text=None,data='delete_ex')
        ])

    template_message = TemplateSendMessage(alt_text='功能',template=buttons_template)
    line_bot_api.reply_message(event.reply_token,template_message)


def delivery_ex(event):
    try:
        ID = event.source.group_id
    except:
        ID = event.source.user_id
    line_bot_api.push_message(ID,TextMessage(text="請輸入資料 以下是範例"))
    line_bot_api.reply_message(event.reply_token,TextMessage(text="外送者:沈育全\n外送地區:大社\n收單時間:0301 1700\n送達時間:0301 1900\n上限份數:10\n取貨地點:燕窩136"))

def delivery_input(event):
    result = event.message.text
    d = result.find("外送者:")
    a = result.find("外送地區:")
    rt = result.find("收單時間:")
    dt = result.find("送達時間:")
    lim = result.find("上限份數:")
    place = result.find("取貨地點:")
    now = datetime.now()+timedelta(hours = 8)
    now = datetime.strftime(now,"%m%d %H%M")
    if(d !=-1 and a !=-1 and rt!=-1 and dt!=-1 and lim!=-1 and place!=-1):
        result = result.split("\n")
        if(len(result)==6):
            ID = event.source.user_id
            try:
                rt = sp(result[2])
                dt = sp(result[3])
                lim = sp(result[4])
                datetime.strptime(rt,"%m%d %H%M")
                print(rt)
                datetime.strptime(dt,"%m%d %H%M")
                int(lim)
                print(dt)
                print(now)
                if(rt<now or dt< now):
                    line_bot_api.reply_message(event.reply_token,TextMessage(text="時間輸入錯誤"))
                else:
                    ID = Delivery_add(sp(result[0]),"",sp(result[1]),rt,dt,lim,sp(result[5]),"0",ID)
                    replytext = "已收到感謝您的使用\n您的訂單編號是:" + ID
                    line_bot_api.reply_message(event.reply_token,TextMessage(text=replytext))
            except:
                line_bot_api.reply_message(event.reply_token,TextMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextMessage(text="輸入錯誤"))
    else:
        line_bot_api.reply_message(event.reply_token,TextMessage(text="輸入錯誤"))
def user_ex(event):
    try:
        ID = event.source.group_id
    except:
        ID = event.source.user_id
    line_bot_api.push_message(ID,TextMessage(text="請輸入資料 以下是範例"))
    line_bot_api.reply_message(event.reply_token,TextMessage(text="使用者:ZOZEJ\n外送地區:大社\n送達時間:0301 1900\n店家:碳烤土司\n點餐內容:二號餐*1 3號餐*1\n總份數:2"))

def user_input(event):
    replytext="已收到感謝您的使用\n您的訂單編號是:"
    result = event.message.text
    now = datetime.now()+timedelta(hours = 8)
    now = datetime.strftime(now,"%m%d %H%M")
    u = result.find("使用者:")
    a = result.find("外送地區:")
    dt = result.find("送達時間:")
    s = result.find("店家:")
    p = result.find("點餐內容:")
    q = result.find("總份數:")
    if(u !=-1 and a !=-1 and dt!=-1 and s!=-1 and p!=-1 and q !=-1):
        result = result.split("\n")
        if(len(result)==6):
            UserID = event.source.user_id
            try:
                dt = sp(result[2])
                q = sp(result[5])
                datetime.strptime(dt,"%m%d %H%M")
                int(q)
                if(dt<now):
                    line_bot_api.reply_message(event.reply_token,TextMessage(text="時間輸入錯誤"))
                else:
                    ID = UserInputCheck(sp(result[0]),sp(result[1]),sp(result[2]),sp(result[3]),sp(result[4]),sp(result[5]),UserID)
                if(ID!="目前沒有可以媒合的對象"):
                    replytext = replytext + ID
                else:
                    replytext = ID
                line_bot_api.reply_message(event.reply_token,TextMessage(text=replytext))
            except:
                line_bot_api.reply_message(event.reply_token,TextMessage(text="輸入錯誤"))  
        else:
            line_bot_api.reply_message(event.reply_token,TextMessage(text="輸入錯誤"))  
    else:
        line_bot_api.reply_message(event.reply_token,TextMessage(text="輸入錯誤"))
        
def searchall(event):
    try:
        ID = event.source.group_id
    except:
        ID = event.source.user_id
    r = readall()
    if (r ==[]):
        line_bot_api.reply_message(event.reply_token,TextMessage(text = "目前查無訂單"))
    else:
        for x in range(0,len(r),10):
            readresult = "OrderID:"+r[x]+"\n地區:"+r[x+1]+"\n外送者:"+r[x+2]+"\n使用者:"+r[x+3]+"\n收單時間:"+r[x+4]+"\n送達時間:"+r[x+5]+"\n上限份數:"+r[x+6]+"\n訂單明細:"+r[x+7]+"\n目前總份數:"+r[x+8]+"\n取貨地點:"+r[x+9]
            line_bot_api.push_message(ID,TextMessage(text = "查詢結果\n"+readresult))

def search(event):
    
    try:
        G_ID = event.source.group_id
        ID = event.source.user_id
        r = read(ID)
        if (r == "查無與您相關資料"):
            line_bot_api.reply_message(event.reply_token,TextMessage(text = "查無與您相關資料"))
        else:
            for x in range(0,len(r),10):
                readresult = "OrderID:"+r[x]+"\n地區:"+r[x+1]+"\n外送者:"+r[x+2]+"\n使用者:"+r[x+3]+"\n收單時間:"+r[x+4]+"\n送達時間:"+r[x+5]+"\n上限份數:"+r[x+6]+"\n訂單明細:"+r[x+7]+"\n目前總份數:"+r[x+8]+"\n取貨地點:"+r[x+9]
                line_bot_api.push_message(G_ID,TextMessage(text = "查詢結果\n"+readresult))
    except:
        ID = event.source.user_id
        r = read(ID)
        if (r == "查無與您相關資料"):
            line_bot_api.reply_message(event.reply_token,TextMessage(text = "查無與您相關資料"))
        else:
            for x in range(0,len(r),10):
                readresult = "OrderID:"+r[x]+"\n地區:"+r[x+1]+"\n外送者:"+r[x+2]+"\n使用者:"+r[x+3]+"\n收單時間:"+r[x+4]+"\n送達時間:"+r[x+5]+"\n上限份數:"+r[x+6]+"\n訂單明細:"+r[x+7]+"\n目前總份數:"+r[x+8]+"\n取貨地點:"+r[x+9]
                line_bot_api.push_message(G_ID,TextMessage(text = "查詢結果\n"+readresult))
    

def delete_ex(event):
    try:
        ID = event.source.group_id
    except:
        ID = event.source.user_id
    line_bot_api.push_message(ID,TextMessage(text= "請輸入要刪除的訂單編號，僅有使用者可以刪除與自已相關的訂單，以下是範例"))
    line_bot_api.reply_message(event.reply_token,TextMessage(text = "刪除訂單編號:0"))

def delete(event):
    ID = event.source.user_id
    result = event.message.text
    O_ID = sp(result)
    d_result = deleteOrder(O_ID,ID)
    line_bot_api.reply_message(event.reply_token,TextMessage(text=d_result))


def sp(data):
    s = data
    w = s.find(":")
    return(s[w+1::])

import os
if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
    app.run(host='0.0.0.0',port=os.environ['PORT'])
    
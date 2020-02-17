# encoding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from dbAdd import Delivery_add,User_add,UserInputCheck,UserUpdates,InputEndCheck,read,readall

app = Flask(__name__)

# 填入你的 message api 資訊
line_bot_api = LineBotApi('N97P2OvLyWzhxJHNQgLpCUymUSkNMdiSQBqKgaOXBU5AAVOMuTNbA1whs1Ocy4Ozk2hsFoUbvn+KicYgFT24DKdArnej2tne/q31PvbeahGjKcnIMuBkOECg2Df6TXMbBvupbgxTnAXqDcpyKgylSgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('38d5c2f5185a44fa17ffe21e3788ccc2')



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
    
    if content =="功能12":
        function(event)
        
        user_id = event.source.user_id
        print("user_id =", user_id)
        #外送群組ID
        #line_bot_api.push_message("Cd495babd31cff04b3743958031d8dd71",TextMessage(text="g"))
        #我跟bot的對話框
        line_bot_api.push_message("U879fdf1cc34bb4c11099be8ffb9b6bb8",TextMessage(text="有人在玩我"))
        

    elif content.find("可外帶")!=-1:
        delivery_ex(event)
    
    elif content.find("外送者")!=-1:
        delivery_input(event)

    elif content.find("幫外帶")!=-1:
        user_ex(event)

    elif content.find("使用者")!=-1:
        user_input(event)

    elif content == "查詢訂單":
        search(event)

    elif content =="查詢全部":
        searchall(event)

    else:
        pass

def delivery_ex(event):
    #line_bot_api.push_message("Cd495babd31cff04b3743958031d8dd71",TextMessage(text="請輸入資料 以下是範例"))
    line_bot_api.reply_message(event.reply_token,TextMessage(text="外送者:沈育全\n外送地區:大社\n收單時間:1700\n送達時間:1900\n上限份數:10\n取貨地點:燕窩136"))

def delivery_input(event):
    result = event.message.text
    result = result.split("\n")
    ID = Delivery_add(sp(result[0]),"",sp(result[1]),sp(result[2]),sp(result[3]),sp(result[4]),sp(result[5]),"0")
    replytext = "已收到感謝您的使用\n您的訂單編號是:" + ID
    line_bot_api.reply_message(event.reply_token,TextMessage(text=replytext))

def user_ex(event):
    #line_bot_api.push_message("Cd495babd31cff04b3743958031d8dd71",TextMessage(text="請輸入資料 以下是範例"))
    line_bot_api.reply_message(event.reply_token,TextMessage(text="使用者:ZOZEJ\n外送地區:大社\n送達時間:1900\n店家:碳烤土司\n點餐內容:二號餐*1 3號餐*1\n總份數:2"))

def user_input(event):
    replytext="已收到感謝您的使用\n您的訂單編號是:"
    result = event.message.text
    result = result.split("\n")
    UserID = event.source.user_id
    print(UserID)
    UserInputCheck(sp(result[0]),sp(result[1]),sp(result[2]),sp(result[3]),sp(result[4]),sp(result[5]),UserID)
    ID = InputEndCheck(1,sp(result[0]))
    if(ID!=[]):
        for x in ID:
            replytext = replytext + str(x)
    else:
        replytext = "目前沒有可以與您媒合的訂單"
    line_bot_api.reply_message(event.reply_token,TextMessage(text=replytext))

def searchall(event):
    r = readall()
    if (r ==[]):
        line_bot_api.push_message("U879fdf1cc34bb4c11099be8ffb9b6bb8",TextMessage(text = "目前查無訂單"))
    else:
        for x in range(0,len(r),10):
            readresult = "OrderID:"+r[x]+"\n地區:"+r[x+1]+"\n外送者:"+r[x+2]+"\n使用者:"+r[x+3]+"\n收單時間:"+r[x+4]+"\n送達時間:"+r[x+5]+"\n上限份數:"+r[x+6]+"\n訂單明細:"+r[x+7]+"\n目前總份數:"+r[x+8]+"\n取貨地點:"+r[x+9]
            line_bot_api.push_message("U879fdf1cc34bb4c11099be8ffb9b6bb8",TextMessage(text = "查詢結果\n"+readresult))

#TODO 有問題
def search(event):
    U_ID = event.source.user_id
    r = read(U_ID)
    if (r ==[]):
        line_bot_api.push_message("U879fdf1cc34bb4c11099be8ffb9b6bb8",TextMessage(text = "查無與您相關資料"))
    else:
        for x in range(0,len(r),10):
            readresult = "OrderID:"+r[x]+"\n地區:"+r[x+1]+"\n外送者:"+r[x+2]+"\n使用者:"+r[x+3]+"\n收單時間:"+r[x+4]+"\n送達時間:"+r[x+5]+"\n上限份數:"+r[x+6]+"\n訂單明細:"+r[x+7]+"\n目前總份數:"+r[x+8]+"\n取貨地點:"+r[x+9]
            line_bot_api.push_message("U879fdf1cc34bb4c11099be8ffb9b6bb8",TextMessage(text = "查詢結果\n"+readresult))
            

def function(event):
    line_bot_api.reply_message(event.reply_token,TextMessage(text="直接輸入想要使用的功能，系統會提供範例，請複製範例再進行修改\n目前的功能有:\n可外帶(司機)\n幫外帶(使用者)\n查詢清單"))

def sp(data):
    s = data
    w = s.find(":")
    return(s[w+1::])

import os
if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
    app.run(host='0.0.0.0',port=os.environ['PORT'])
    

from dbModel import Order,OrderDetail
from sqlalchemy import create_engine,or_
from sqlalchemy.orm import sessionmaker
from datetime import datetime,timedelta
import re


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
database = create_engine("postgres://idojhmutgwujgs:86290065805ef7e22a3329f7d8e12bac3de18f730a93a1ce856da810c61e3603@ec2-54-243-47-196.compute-1.amazonaws.com:5432/df02edp9fag4h2")
DB_session = sessionmaker(database)
db_session = DB_session()

line_bot_api = LineBotApi('N97P2OvLyWzhxJHNQgLpCUymUSkNMdiSQBqKgaOXBU5AAVOMuTNbA1whs1Ocy4Ozk2hsFoUbvn+KicYgFT24DKdArnej2tne/q31PvbeahGjKcnIMuBkOECg2Df6TXMbBvupbgxTnAXqDcpyKgylSgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('38d5c2f5185a44fa17ffe21e3788ccc2')



now = datetime.now()+timedelta(hours=8)
n1 = now.strftime('%m%d%H%M')
print(n1)

def Delivery_add(d_name,u_name,area,r_time,d_time,limit,place,check,u_id):
    data = Order(Delivery_name = d_name, User_name= u_name, Area = area, Receipt_time = r_time, Delivery_time = d_time
                , Limit = limit, Place = place, Check = check,User_ID = u_id)
    db_session.add(data)
    db_session.commit()
    print(data.OrderID)
    print("Delivery Add DONE")





def sp(data):
    s = data
    w = s.find(":")
    if(w==-1):
        return False
    return(s[w+1::])

"""
Delivery_add(sp(text),"","大社","1900","2030","5","133","0","123456")
db_session.commit()
db_session.close()
"""

def UserUpdates(id):
    db_session.query(Order).filter(Order.OrderID==39).update({"User_ID":id})
    print("Updates DONE")
    db_session.commit()
    db_session.close()
#UserUpdates("123456")
def test(uid):
    
    getresult = db_session.query(Order.OrderID.label("oid"),Order.User_ID.label("ou_id"),OrderDetail.UserID.label("du_id")).join(OrderDetail,OrderDetail.OrderID == Order.OrderID,isouter=True).filter((Order.User_ID == uid)|(OrderDetail.UserID==uid))
    i = iter(getresult)
    gr = next(i)
    print(gr.oid)
    print(gr.ou_id)
    print(gr.du_id)
    print("done")  



def search():
    U_ID = "U879fdf1cc34bb4c11099be8ffb9b6bb8"

    getresult = db_session.query(Order.OrderID.label("oid"),Order.Area.label("area"),Order.Delivery_name.label("d_name"),Order.User_name.label("u_name")
    ,Order.Receipt_time.label("r_time"),Order.Delivery_time.label("d_time"),Order.Limit.label("limit"),Order.Place.label("place"),OrderDetail.Store_name.label("s_name"),
    OrderDetail.Product.label("product"),OrderDetail.Quantity.label("q")).join(OrderDetail,OrderDetail.OrderID == Order.OrderID,isouter=True).filter((OrderDetail.UserID== U_ID)|(Order.User_ID==U_ID)).order_by(Order.OrderID)


    result = []
    product = ""
    quantity = 0
    count = 0


    i = iter(getresult)

    while True:
        try:
            if(count ==0):
                gr = next(i)
                gr1 = next(i)
                count += 1
            else:
                gr = gr1
                gr1 = next(i)

            product = product + gr.s_name + "," + gr.product + "  " 
            quantity = quantity + int(gr.q) 
            
            if(gr.oid!=gr1.oid):
                result.append(str(gr.oid))
                result.append(gr.area)
                result.append(gr.d_name)
                result.append(gr.u_name)
                result.append(gr.r_time)                 
                result.append(gr.d_time)
                result.append(gr.limit)
                result.append(product)
                result.append(str(quantity))
                result.append(gr.place)
                print(result)
                product = ""
                quantity = 0
        except:
            if(count==0):
                break
            product = product + gr.s_name + "," + gr.product + "  " 
            quantity = quantity + int(gr.q) 
            result.append(str(gr.oid))
            result.append(gr.area)
            result.append(gr.d_name)
            result.append(gr.u_name)
            result.append(gr.r_time) 
            result.append(gr.d_time)
            result.append(gr.limit)
            result.append(product)
            result.append(str(quantity))
            result.append(gr.place)
            print(result)
            break

"""
#查詢現在所有的訂單(可全部獲現在時間之後的)
def readall():
    d_ID = ""
    product =""
    quantity = 0
    now = datetime.now()+timedelta(hours = 8)
    n1 = now.strftime('%H%M')
    result = []
    for o in db_session.query(Order).filter(n1<Order.Receipt_time).order_by(Order.OrderID):
        result.append(str(o.OrderID))
        result.append(o.Area)
        result.append(o.Delivery_name)
        result.append(o.User_name)
        result.append(o.Receipt_time) 
        result.append(o.Delivery_time)
        result.append(o.Limit)
        
        for d in db_session.query(OrderDetail).filter(o.OrderID == OrderDetail.OrderID):
            product = product + d.Store_name + "," + d.Product + " "
            quantity = quantity + int(d.Quantity)
            d_ID = d.OrderID
        if(o.OrderID ==d_ID):
            result.append(product)
            result.append(str(quantity))
            result.append(o.Place)
        else:
            result.append(" ")
            result.append(" ")
            result.append(o.Place)
    return result
"""




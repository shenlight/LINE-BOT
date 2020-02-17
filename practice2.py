
from dbModel import Order,OrderDetail
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
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






def UserUpdates(name,id):
    db_session.query(Order).filter(Order.OrderID==id).update({"User_name":name})
    print("Updates DONE")
    db_session.commit()
    db_session.close()
try:
    UserUpdates("",36,123)
except(TypeError):
    print("輸入錯誤")


def search():
    U_ID = "U879fdf1cc34bb4c11099be8ffb9b6bb8"

    getresult = db_session.query(Order.OrderID.label("oid"),Order.Area.label("area"),Order.Delivery_name.label("d_name"),Order.User_name.label("u_name")
    ,Order.Receipt_time.label("r_time"),Order.Delivery_time.label("d_time"),Order.Limit.label("limit"),Order.Place.label("place"),OrderDetail.Store_name.label("s_name"),
    OrderDetail.Product.label("product"),OrderDetail.Quantity.label("q")).join(OrderDetail,OrderDetail.OrderID == Order.OrderID,isouter=True).filter(OrderDetail.UserID== U_ID).order_by(Order.OrderID)

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

def Delivery_add(d_name,u_name,area,r_time,d_time,limit,place,check):
    data = Order(Delivery_name = d_name, User_name= u_name, Area = area, Receipt_time = r_time, Delivery_time = d_time
                , Limit = limit, Place = place, Check = check)
    db_session.add(data)
    db_session.commit()
    print(data.OrderID)
    print("Delivery Add DONE")
"""
Delivery_add("小雞","","大社","1900","2030","5","133","0")
db_session.query(Order).filter(Order.OrderID==37).delete()
print("delete done")
db_session.commit()
db_session.close()
"""

"""
#book_list = db_session.query(Book.name.label("bname"),Author.name.label ("aname")).join(Author,Book.author_id == Author.id,isouter=True).all()
result = db_session.query(Order.OrderID.label("oid"),Order.Area.label("area"),Order.Delivery_name.label("d_name"),Order.User_name.label("u_name")
,Order.Receipt_time.label("r_time"),Order.Delivery_time.label("d_time"),Order.Limit.label("limit"),Order.Place.label("place"),OrderDetail.Store_name.label("s_name"),
OrderDetail.Product.label("product"),OrderDetail.Quantity.label("q")).join(OrderDetail,OrderDetail.OrderID == Order.OrderID and OrderDetail.UserID== U_ID,isouter=True).all()
for row in result:
    print(row)
"""



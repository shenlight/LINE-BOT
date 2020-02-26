from dbModel import Order,OrderDetail
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime,timedelta
import re
database = create_engine("postgres://idojhmutgwujgs:86290065805ef7e22a3329f7d8e12bac3de18f730a93a1ce856da810c61e3603@ec2-54-243-47-196.compute-1.amazonaws.com:5432/df02edp9fag4h2")
DB_session = sessionmaker(database)
db_session = DB_session()

#司機新增
def Delivery_add(d_name,u_name,area,r_time,d_time,limit,place,check,u_id):
    data = Order(Delivery_name = d_name, User_name= u_name, Area = area, Receipt_time = r_time, Delivery_time = d_time
                , Limit = limit, Place = place, Check = check,User_ID = u_id)
    db_session.add(data)
    db_session.commit()
    ID = str(data.OrderID)
    db_session.close()
    print("Delivery Add DONE")
    return ID
#delivery_add("西班牙","","高雄","1700","1930","5","133")

#使用者新增
def User_add(orderid,u_name,store,prduct,quantity,u_id):
    data = OrderDetail(OrderID = orderid,User_name = u_name,Store_name = store,Product = prduct,Quantity = quantity,UserID =u_id)
    db_session.add(data)
    db_session.commit()
    ID = str(data.OrderID)
    db_session.close()
    print("User Add DONE")
    return ID
#User_add("2","呆毛","鮮茶道","文山青無糖微冰","1")

#使用者新增後更新Order使用者欄位
def UserUpdates(name,id):
    db_session.query(Order).filter(Order.OrderID==id).update({"User_name":name})
    print("Updates DONE")
    db_session.commit()
    db_session.close()
#updates("",6)

#使用者輸入時間檢查有無可以媒合的對象
def UserInputCheck(name,area,d_time,store,product,quantity,u_id):
    check = db_session.query(Order).filter(Order.Area==area).order_by(Order.OrderID)
    now = datetime.now()+timedelta(hours=8)
    n1 = now.strftime('%H%M')
    
    #檢查是否超過結單時間與送達時間
    for row in check:
        d_time1 = datetime.strptime(d_time,'%H%M')+timedelta(minutes=30)
        d_time1 = datetime.strftime(d_time1,'%H%M')
        if(n1<row.Receipt_time and d_time<=row.Delivery_time<=d_time1):
            ID = row.OrderID
            Limit = int(row.Limit)
            result = db_session.query(OrderDetail).filter(OrderDetail.OrderID == ID).all()
            count = 0
            Name = row.User_name
            #檢查是否超過Delivery設定數量上限
            for q in result:
                count = int(q.Quantity)+count
                print(count)
            count += int(quantity)
            print(count)
            if(count<=Limit):
                rU_ID = User_add(ID,name,store,product,quantity,u_id)
                name = Name+","+name
                UserUpdates(name,ID)
                print("check Done")
                return rU_ID
            else:
                print("over count")
        else:
            print("no data1")
    return "目前沒有可以媒合的對象"
#UserInputCheck("Yes234","高雄","1800","麻辣燙","米血豆干小雞",1)

#查詢訂單 依訂單編號
def read(U_ID):
    result = []
    product = ""
    quantity = 0
    count = 0

    getresult = db_session.query(Order.OrderID.label("oid"),Order.Area.label("area"),Order.Delivery_name.label("d_name"),Order.User_name.label("u_name")
    ,Order.Receipt_time.label("r_time"),Order.Delivery_time.label("d_time"),Order.Limit.label("limit"),Order.Place.label("place"),OrderDetail.Store_name.label("s_name"),
    OrderDetail.Product.label("product"),OrderDetail.Quantity.label("q")).join(OrderDetail,OrderDetail.OrderID == Order.OrderID,isouter=True).filter((OrderDetail.UserID== U_ID)|(Order.User_ID==U_ID)).order_by(Order.OrderID)

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

            if(gr.s_name is not None):
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
                product = ""
                quantity = 0
        except(StopIteration):
            if(count==0):
                return "查無與您相關資料"
            if(gr.s_name is not None):
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
            return result
#clock用單筆查詢

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

def deleteOrder(ID,U_ID):
    ID = int(ID)
    result = db_session.query(OrderDetail.User_name.label("u_name")).filter(OrderDetail.OrderID==ID and OrderDetail.UserID==U_ID)
    try:
        i = iter(result)
        gr = next(i)
        du_name = gr.u_name
        print(du_name)

        result1 = db_session.query(Order.User_name.label("u_name")).filter(Order.OrderID==ID)
        i = iter(result1)
        gr = next(i)
        u_name = gr.u_name
        u_name = re.sub(","+du_name,'',u_name)
        print(u_name)

        UserUpdates(u_name,ID)
        db_session.query(OrderDetail).filter(OrderDetail.OrderID==ID).delete()
        db_session.commit()
        db_session.close()
        print("delete done")
        return "刪除完成"
    except(StopIteration):
        return "刪除失敗"
    except(TypeError):
        return "刪除失敗"


#每隔一段時間資料庫將發現符合條件的資料輸出 並做記號
def TimeCheck():
    result = []
    quantity = 0
    product = ""
    now = datetime.now()+timedelta(hours = 8)
    now = now.strftime('%H%M')
    for o in db_session.query(Order).filter(Order.User_name!="" ,now>Order.Receipt_time ,Order.Check!="1").order_by(Order.OrderID):
        result.append(str(o.OrderID))
        result.append(o.Area)
        result.append(o.Delivery_name)
        result.append(o.User_name)
        result.append(o.Receipt_time) 
        result.append(o.Delivery_time)
        result.append(o.Limit)
        
        for d in db_session.query(OrderDetail).filter(OrderDetail.OrderID == o.OrderID):
            product = product + d.Store_name + "," + d.Product + " "
            quantity = quantity + int(d.Quantity)
            
        db_session.query(Order).filter(Order.OrderID == o.OrderID).update({"Check":"1"})
        db_session.commit()
        db_session.close()
        result.append(product)
        result.append(str(quantity))
        result.append(o.Place)
        quantity = 0
        product = ""
    if(result!=[]):
        return result
    else:
        return "查無資料"


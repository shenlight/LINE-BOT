from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Order(db.Model):
    __tablename__ = 'Order'

    OrderID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Delivery_name = db.Column(db.String(256))
    User_name = db.Column(db.String(256))
    Area = db.Column(db.String(128))
    Receipt_time = db.Column(db.String(128))
    Delivery_time = db.Column(db.String(128))
    Limit = db.Column(db.String(64))
    Place = db.Column(db.String(256))
    Check = db.Column(db.String(32))
    User_ID = db.Column(db.String(256))

    def __init__(self
                 , Delivery_name
                 , User_name
                 , Area
                 , Receipt_time
                 , Delivery_time
                 , Limit
                 , Place
                 , Check
                 , User_ID
                 ):
        self.Delivery_name = Delivery_name
        self.User_name = User_name
        self.Area = Area
        self.Receipt_time = Receipt_time
        self.Delivery_time = Delivery_time
        self.Limit = Limit
        self.Place = Place
        self.Check = Check
        self.User_ID = User_ID

class OrderDetail(db.Model):
    __tablename__ = 'OrderDetail'
    ID = db.Column(db.Integer,primary_key=True,autoincrement=True,)
    OrderID = db.Column(db.Integer,db.ForeignKey("Order.OrderID"))
    User_name = db.Column(db.String(256))
    Store_name = db.Column(db.String(256))
    Product = db.Column(db.String(256))
    Quantity = db.Column(db.String(32))
    UserID = db.Column(db.String(256))
    def __init__(self
                 , OrderID
                 , User_name
                 , Store_name
                 , Product
                 , Quantity
                 , UserID
                 ):
        self.OrderID = OrderID
        self.User_name = User_name
        self.Store_name = Store_name
        self.Product = Product
        self.Quantity = Quantity
        self.UserID = UserID

if __name__ == '__main__':
    manager.run()
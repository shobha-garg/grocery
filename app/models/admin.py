from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Admin(db.Model):
    __tablename__='admin'
    uid = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable= False)
    phone = db.Column(db.Integer, nullable= False, unique=True)
    password = db.Column(db.String, nullable= False)
    
class User(db.Model):
    __tablename__='user'
    user_id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    users = db.relationship('Cart',backref='user',lazy=True)
    
class Product(db.Model):
    __tablename__ = "product"
    pid = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True, nullable= False)
    product_name = db.Column(db.String, nullable= False, unique= True)
    filepath= db.Column(db.String, nullable= False)
    price = db.Column(db.Integer, nullable= False)
    quantity = db.Column(db.Integer, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("section.sid"))
    products = db.relationship('Cart',backref='product',lazy=True)
    
class Section(db.Model):
    __tablename__= "section"
    sid = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True, nullable= False)
    section_name = db.Column(db.String, nullable= False, unique= True)
    products= db.relationship('Product',backref='section',lazy=True,)
    
class Cart(db.Model):
    __tablename__="cart"
    cid= db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True, nullable= False)
    user_id= db.Column(db.Integer, db.ForeignKey("user.user_id"))
    product_id= db.Column(db.Integer, db.ForeignKey("product.pid"))
    name= db.Column(db.String)
    Price= db.Column(db.Integer)
    Quantity= db.Column(db.Integer, nullable= False)
    
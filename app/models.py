from flask_user import login_required, UserManager, UserMixin
from sqlalchemy import Table, Column, String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

 # Bind users and organizations
users_orgs_association_table = db.Table("users_orgs_association",
                                        db.Column("org_id",
                                                  db.Integer,
                                                  db.ForeignKey("organizations.id", ondelete="CASCADE")),
                                        db.Column("user_id",
                                                  db.Integer,
                                                  db.ForeignKey("users.id", ondelete="CASCADE")))


class Organization(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    data_dir = db.Column(db.String(200), unique=True, index=True)
    users = db.relationship("User",
                         secondary=users_orgs_association_table,
                         back_populates="organizations")
    fixed_totalizers = db.relationship("FixedTotalizer", cascade="delete")
    free_functions = db.relationship("FreeFunction", cascade="delete")
    groups = db.relationship("Group", cascade="delete")
    departments = db.relationship("Department", cascade="delete")
    taxes = db.relationship("Tax", cascade="delete")
    plus = db.relationship("PLU", cascade="delete")
    clerks = db.relationship("Clerk", cascade="delete")
    customers = db.relationship("Customer", cascade="delete")
    orders = db.relationship("Order", cascade="delete")




class Master(db.Model):
    """Base class for Master files data (abstract class, not a table)"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    date_time = db.Column(db.DateTime, nullable=False)
    filepath = db.Column(db.String(100), nullable=False)
    data_dir = db.Column(db.String(100), nullable=False)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    organizations = db.relationship("Organization",
                                 secondary=users_orgs_association_table,
                                 back_populates="users")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# @login.user_loader
# def load_user(id):
#     user_id = db.session.query(User).get(int(id))

#     return user_id




class Tax(Master):
    __tablename__ = "taxes"

    org_id = db.Column(db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"))
    name = db.Column(db.String(50))
    rate = db.Column(db.Integer)
    plus = relationship("PLU", back_populates="tax")

    def __repr__(self):
        return "Tax: id=%s number=%s name=%s rate=%s" % (
            self.id, self.number, self.name, self.rate)


class PLU(Master):
    __tablename__ = "plu"

    org_id = db.Column(db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"))
    name = db.Column(db.String(50))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=True)
    group = relationship("Group", back_populates="plus")
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True)
    department = relationship("Department", back_populates="plus")
    price = db.Column(db.Float)
    tax_id = db.Column(db.Integer, db.ForeignKey("taxes.id"), nullable=True)
    tax = relationship("Tax", uselist=False, back_populates="plus")
    orderlines = relationship("OrderLine", backref="plu", lazy="dynamic")

    def __repr__(self):
        return "PLU: id=%s name=%s number=%s group_number=%s department_number=%s price=%s" % (
                self.id, self.name, self.number, self.group_id, self.department_id, self.price)

# >>>>>>>>>>>>>>>>


# Product			
# ID	Name	DeptID*	GroupID*
class Product(db.Model):
	__tablename__ = "products"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	dept_id = db.Column(db.Integer, db.ForeignKey("departments.id", ondelete="CASCADE"))
	group_id = db.Column(db.Integer, db.ForeignKey("groups.id", ondelete="CASCADE"))
	
	def __repr__(self):
		return "Product: id=%s name=%s" % (
            self.id, self.name)


# Department		
# ID	Name	GroupID*


class Department(db.Model):
	__tablename__ = "departments"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	group_id = db.Column(db.Integer, db.ForeignKey("groups.id", ondelete="CASCADE"))
	

	def __repr__(self):
		return "Department: id=%s name=%s" % (
            self.id, self.name)



# Group	
# ID	Name
class Group(db.Model):
	__tablename__ = "groups"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	

	def __repr__(self):
		return "Group: id=%s name=%s" % (
            self.id, self.name)


# Free Function		
# ID	Description	MainFunction
class FreeFunction(db.Model):
	__tablename__ = "free_functions"
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(100))
	main_function = db.Column(db.String(100))
	

	def __repr__(self):
		return "FreeFunction: id=%s description=%s" % (
            self.id, self.description)


# Fixed Totalizer	
# ID	Descrition
class FixedTotalizer(db.Model):
    __tablename__ = "fixed_totalizers"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))

    def __repr__(self):
    	return "Fixed Totalizer: id=%s description=%s" % (
                self.id, self.description)


# Clerk	
# ID	Name
class Clerk(db.Model):
    __tablename__ = "clerks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    def __repr__(self):
        return "Clerk: id=%s name=%s" % (self.id, self.name)


# Machine	
# ID	Name
class Machine(db.Model):
    __tablename__ = "machines"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    def __repr__(self):
        return "Clerk: id=%s name=%s" % (self.id, self.name)


# Customer			
# ID	FirstName	Surname	Address1
class Customer(Master):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    addr1 = db.Column(db.String(100))
    
    def __repr__(self):
        return "Customer: id=%s first_name=%s surname=%s surname=%s" % (self.id, self.first_name, self.surname, self.addr1)




# Order									
# ID	Date	Time	TableNo	ClerkID*	CustomerID*	ConsNo	Cover	Status	Mode
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    table_number = db.Column(db.Integer)
    clerk_id = db.Column(db.Integer, db.ForeignKey("clerks.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=True)
    consecutive_number = db.Column(db.Integer)
    cover = db.Column(db.String(50))
    status = db.Column(db.String(50))
    mode = db.Column(db.String(50))

    def __repr__(self):
    	return "Order: ID=%s" % (self.id)


# OrderLines						
# ID	OrderID*	ProdID*	Qty	Value	TaxID*	MixMatchID*
class OrderLine(db.Model):
    __tablename__ = "order_lines"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("plu.id"), nullable=True)
    qty = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
    tax_id = db.Column(db.Integer, db.ForeignKey("taxes.id"), nullable=True)


    def __repr__(self):
        return "OrderLine: id=%s order_id=%s product_id=%s qty=%s value=%s" % (
                self.id, self.order_id, self.product_id, self.qty, self.value)

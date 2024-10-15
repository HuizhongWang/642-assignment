"""! @brief Fresh Harvest Veggies with Doxygen style comments"""

##
# @mainpage Fresh Harvest Veggies Project
# @section description_main Description
# Fresh Harvest Veggies is a company based in Lincoln that sells high quality farm-fresh 
# vegetables.

##
# @file define.py
#
# @brief Example Python with Doxygen
#
# @section auther_define Author
# Created by Huizhong Wang on 27/09/2024

# Imports
from abc import ABC
from typing import List
from datetime import date
from flask import Flask,flash,render_template,request,session,redirect,url_for,g
from flask_hashing import Hashing
import sqlalchemy

# connect database
engine = sqlalchemy.create_engine('mysql://root:mina!612@localhost/test',echo=True)
conn = engine.connect()

class User(ABC):
    """
    @brief Abstract base class representing a user.
    """
    def __init__(self, type: int, fname: str, lname: str, password:str):
        """! The class initialiser
        @brief Constructor for User.
        @param type The type of user (1 for private customer, 2 for corporate customer, 3 for staff).
        @param fname First name of the user.
        @param lname Last name of the user.
        @param password.
        """
    
        ## This is the user type
        self._type = type
        ## This is the first name of user
        self._fname = fname
        ## This is the last name of user
        self._lname = lname
        ## This is the password of user
        self._password = password

    def login():
        connection = getCursor()
        # get the login info
        if request.method == 'POST' and 'userid' in request.form and 'pwd' in request.form:
            userid = int(request.form['userid'])
            userpwd = request.form['pwd']
            connection.execute('SELECT * FROM users WHERE forester_id = %s or staff_id = %s', (userid,userid,))
            user = connection.fetchone()

            # if the userid is existed
            if user is not None:
                password = user[3]  # database pwd
                if hashing.check_value(password, userpwd, salt='abc'): # if the userid and password match
                    session['pwd']=userpwd
                # If account exists in accounts table 
                # Create session data, we can access this data in other routes
                    if user[1]:
                        session['userid'] = user[1]
                        session['role'] = "forester"
                        session['status'] = user[4]
                        return redirect(url_for('forester.f_index'))
                    elif user[2] and user[0]=="staff":
                        session['userid'] = user[2]
                        session['role'] = "staff"
                        session['status'] = user[4]
                        return redirect(url_for('staff.s_index'))
                    elif user[2] and user[0]=="admin":
                        session['userid'] = user[2]
                        session['role'] = "admin"
                        session['status'] = user[4]
                        return redirect(url_for('admin.a_index'))
                else:
                    #password incorrect
                    flash('Incorrect password!',"danger")
            else:
                # Account doesnt exist or username incorrect
                flash('Incorrect ID number',"danger")

        return render_template("index/login.html")


    def logout():
        session.pop("userid", None) 
        return redirect(url_for('home'))
        


class Customer(User):
    """
    @brief Class representing a customer.
    """
    def __init__(self, custId: str, type: int, password:str, fname: str, lname: str, addr: str, custBalance: float, maxOwing: float = 0):
        """
        @brief Constructor for Customer.
        @param radius Delivery radius for the customer.
        @param balance Current balance for the customer.
        @param credit_limit Credit limit for corporate customers (only applicable if type is 2).
        """
        super().__init__(type, fname, lname, password)
        ## This is the id of the customer
        self._id = custId
        ## This is the balance of the customer
        self._balance = custBalance
        ## This is the address of the customer
        self._addr = addr
        ## This is the address of the customer

        self._credit_limit = credit_limit if type == 2 else 0  # Only applicable for corporate customers

    @property
    def type(self):
        return self._type
    
    @property
    def fname(self):
        return self._fname
    
    @property
    def lname(self):
        return self._lname
    
    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value: float):
        """
        @brief update the balance
        @param value: the new balance
        """
        self._balance = value

    def getCustomer(self,name):
        """
        @brief Get the customer data from the database
        @param name: the name of the customer
        @return the detail of the customer
        """
        pass
    
    def checkBalance(self) -> bool:
        """
        @brief Checks if the customer is able to place an order based on their balance.
        @return True if the customer can place an order, False otherwise.
        """
        if self._type == 1:  # Private customer
            return self._balance <= 100
        elif self._type == 2:  # Corporate customer
            return self._balance >= self._credit_limit
        return False

    def getOrderHistory(self) -> List['Order']:
        """
        @brief Retrieves the order history for this customer from the database.
        @return: List[Order] A list of orders specific to this customer.
        """


class Staff(User):
    """
    @brief Class representing a staff member.
    """
    def __init__(self, id: str, fname: str, lname: str, gender: str, phone: str, addr: str):
        """
        @brief Constructor for Staff.
        @param role The role of the staff member (e.g., manager, cashier).
        @param salary The salary of the staff member.
        """
        super().__init__(id, 3, fname, lname, gender, phone, addr)  # type 3 indicates staff
    
    @property
    def id(self):
        return self._id
    

class Products:
    """
    @brief Class representing a product.
    """
    def __init__(self, id: int, pname: str, type: int, price: float, unit: str, inventory: int):
        """
        @brief Constructor for Products.
        @param id: int Product ID.
        @param pname Name of the product.
        @param type Product type (0: individual, 1: premade box).
        @param price Price of the product.
        @param unit Unit of the product (e.g., kg, pack).
        @param inventory Current stock of the product.
        """
        ## This is the id of the product
        self._id = id
        ## This is the name of the product
        self._product_name = pname
        ## This is the type of the product
        self._type = type 
        ## This is the price of the product
        self._price = price
        ## This is the unit of the product
        self._unit = unit
        ## This is the inventory of the product
        self._inventory = inventory
    
    @property
    def id(self):
        return self._id
    
    @property
    def inventory(self):
        return self._inventory
    
    @property
    def price(self):
        return self._price
    
    def inventory_reduce(self, num: int):
        """
        @brief Reduces the inventory of the product by a given amount.
        @param num Number of units to reduce.
        @return: str A message indicating success or failure of inventory reduction.
        """
        if self._inventory >= num:
            self._inventory -= num
            return "Inventory reduced."
        else:
            return "Insufficient inventory."


class PremadeBox(Products):
    """
    @brief Class representing a premade box product.
    """
    def __init__(self, id: int, pname: str, type: int, price: float, unit: str, inventory: int, size: str):
        """
        @brief Constructor for PremadeBox.
        @param size Size of the premade box (small, medium, large).
        """
        super().__init__(id, pname, type, price, unit, inventory)
        ## This is the size of the premade box
        self._size = size
        ## This is the content of the premade box
        self._box_content = []

    def create_box(self, product_id: int, num: int, size:str):
        """
        @brief Adds a product to the premade box if enough inventory is available.
        @param product_id ID of the product to add.
        @param num The quantity of the product.
        @param size Size of the box.
        @return: str A message indicating success or failure of adding items to the box.
        """
        if self.inventory >= num:
            self._box_content.append((product_id, num, size))
            return "Box updated."
        else:
            return f"Insufficient inventory: only {self.inventory} left."


class OrderItem:
    """
    @brief Class representing an item in an order.
    """
    def __init__(self, id: int, pname: str, num: int):
        """
        @brief Constructor for OrderItem.
        @param id: int The item ID.
        @param pname Name of the product.
        @param num Quantity of units ordered.
        @param price Price per unit.
        """
        ## This is the item id of the order item
        self._item_id = id
        ## This is the product name of this order item
        self._item_name = pname
        ## This is the purchase quantity of the product
        self._num = num

    def cal_subtotal(self, product) -> float:
        """
        @brief Calculates the subtotal for the order item.
        @param product
        @return The subtotal amount.
        """
        subtotal = self._num * product.price
        return subtotal
    

class Delivery:
    """
    @brief Class representing delivery options.
    """
    def __init__(self, way: int, price:float=0.00):
        """
        @brief Constructor for Delivery.
        @param way Delivery method (1 for delivery, 0 for pick-up).
        """
        self._way = way
        self._delivery_price = price if way == 1 else 0.00
        
    def customer_delivery(self, customer: Customer) -> bool:
        """
        @brief Checks if the customer's address is within the delivery radius.
        @param customer The customer whose address radius needs to be checked.
        @return delivery price, error message otherwise.
        """
        if self.way ==1 and customer._radius <= 20:
            return self.delivery_price
        elif self.way ==0:
            return self.delivery_price
        else:
            raise ValueError("The address is not within the delivery radius.")


class Payment:
    """
    @brief Class representing payment options.
    """
    def __init__(self, method: int):
        """
        @brief Constructor for Payment.
        @param method Payment method (1 for credit card, 2 for debit card, 3 for charging to account).
        @param customer The customer making the payment.
        """
        self._pay_method = method

    def payConfirm(self, customer: Customer, amount: float) -> str:
        """
        @brief Processes the payment based on the selected method.
        @param customer The customer that pays
        @param amount The total amount to be paid.
        @return A message indicating the result of the payment process.
        """
        if self._pay_method == 1:
            # Process credit card payment
            return "Payment processed with credit card."
        elif self._pay_method == 2:
            # Process debit card payment
            return "Payment processed with debit card."
        elif self._pay_method == 3:
            # Process charge to their account
            if customer.balance >= amount:
                customer.balance -= amount
                return "Payment processed by charging to their account."
            else:
                return "Insufficient balance to charge to account."
        else:
            return "Invalid payment method."
        

class Order:
    """
    @brief Class representing a customer order.
    """
    def __init__(self, id: int, order_date: date, staff_id:int, way: int, gst:float, pay_method:int, status:int):
        """
        @brief Constructor for Order.
        @param id The order ID.
        @param order_date The date when the order was placed.
        @param deliver_way The way of delivery(pick-up or delivery)
        @param gst The GST cost
        @param status The status of the order
        @param way Delivery option (1 for delivery, 0 for pick-up).
        """
        ## This is the order id
        self._order_id = id
        ## This is the order date
        self._order_date = order_date
        ## This is the staff that process the order
        self._staff_id = staff_id
        ## This is to show the order is by deliverd or pick up 
        self._delivery_way = way 
        ## This is the gst
        self._gst = gst
        ## This is the payment method of the order
        self._pay_method = pay_method
        ## This is the status of the order
        self._status = status
        ## This is the list of the items in the order
        self._items_list = []

    def add_item(self, item, product):
        """
        @brief Add an order to the order list
        @param product: the choosen product of the item
        @param item: the item of the order
        @return the list of the items in the order
        """
        if product.inventory >= item._num:
            self._items_list.append(item)
            product.inventory_reduce(item._num)
            return "Item added successfully."
        else:
            return "Insufficient stock for this product."

    def cal_total(self, deliver: Delivery,customer:Customer,product:Products) -> float:
        """
        @brief Calculates the total cost of the order.
        @param deliver: the data of delivery
        @param customer: the data of customer
        @param product: the data of products
        @return The total cost of the order including delivery fees and discounts.
        """
        products_total = sum(item.cal_subtotal(product) for item in self._items_list)
        delivery_cost = deliver.customer_delivery(customer)  # Calculate delivery cost
        subtotal = products_total + delivery_cost  # Total before GST and discounts

        if customer.type == 2:  # Apply 10% discount for corporate customers
            subtotal *= 0.9

        self._gst = subtotal*0.15
        total = subtotal + self._gst# Total cost including GST

        return total  

    def create_order(self):
        """
        @brief Create an order
        @return the message showing the order is created or not
        """
        

class Report:
    """
    @brief Class responsible for generating sales reports.
    """
    def total_sales(self, period: str) -> float:
        """
        @brief Generates the total sales report based on the period.
        @param period The period for the report (week, month, or year).
        @return The total sales amount for the given period.
        """
        total_sales = 0.00
        if period == 'week':
            # Calculate total sales for the week
            pass
        elif period == 'month':
            # Calculate total sales for the month
            pass
        elif period == 'year':
            # Calculate total sales for the year
            pass
        return total_sales
    
    def popular_items(self) -> List[str]:
        """
        @brief Generates a report of the most popular items.
        @return A list of the most popular items sold.
        """
        popular_items_list = []  # Store popular items
        # Logic to determine popular items
        return popular_items_list

    def unpopular_items(self) -> List[str]:
        """
        @brief Generates a report of the least popular items.
        @return A list of the least popular items sold.
        """
        unpopular_items_list = []  # Store unpopular items
        # Logic to determine unpopular items
        return unpopular_items_list
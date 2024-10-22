from sqlalchemy import Date, create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Set up database
engine = create_engine('mysql+pymysql://root:mina!612@localhost/fresh',echo=True)
Base = declarative_base()


class Person:
    firstName = Column(String(30))
    lastName = Column(String(30))
    username = Column(String(30), unique=True)
    password = Column(String(10))


class Staff(Person, Base):
    __tablename__ = 'staff'
    staffID = Column(Integer, primary_key=True, unique=True)  
    dateJoined = Column(Date)
    deptName = Column(String(50))


class Customer(Person, Base):
    __tablename__ = 'customers'
    custID = Column(Integer, primary_key=True, autoincrement=True)
    custAddress = Column(String(200))
    custBalance = Column(Float)
    maxOwing = Column(Float)
    
class CorporateCustomer(Customer):
    discountRate = Column(Float, nullable=True)  
    maxCredit = Column(Float)
    minBalance = Column(Float)

# Order class
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    orderCustomer = Column(String(30))
    orderDate = Column(Date)
    orderNumber = Column(Integer)
    orderStatus = Column(String(10))

# PremadeBox class
class PremadeBox(Base):
    __tablename__ = 'premade_boxes'
    id = Column(Integer, primary_key=True)
    boxSize = Column(String(10))
    numOfBoxes = Column(Integer)

# Payment class
class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    paymentAmount = Column(Float)
    paymentDate = Column(Date)

# CreditCardPayment class
class CreditCardPayment(Payment):
    __tablename__ = 'credit_card_payments'
    id = Column(Integer, ForeignKey('payments.id'), primary_key=True)
    cardExpiryDate = Column(Date)
    cardNumber = Column(Integer)
    cardType = Column(String(10))

# DebitCardPayment class
class DebitCardPayment(Payment):
    __tablename__ = 'debit_card_payments'
    id = Column(Integer, ForeignKey('payments.id'), primary_key=True)
    bankName = Column(String(20))
    debitCardNumber = Column(Integer)



# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert 5 staff
staff1 = Staff(firstName="John", lastName="Doe", username="jdoe", password="pass123", dateJoined="2020-01-01", deptName="Sales", staffID="10001")
staff2 = Staff(firstName="Jane", lastName="Smith", username="jsmith", password="pass234", dateJoined="2021-02-15", deptName="HR", staffID="10002")
staff3 = Staff(firstName="Mike", lastName="Brown", username="mbrown", password="pass345", dateJoined="2019-11-23", deptName="IT", staffID="10003")
staff4 = Staff(firstName="Lisa", lastName="White", username="lwhite", password="pass456", dateJoined="2022-07-12", deptName="Finance", staffID="10004")
staff5 = Staff(firstName="Tom", lastName="Black", username="tblack", password="pass567", dateJoined="2018-05-30", deptName="Logistics", staffID="10005")

# Insert 5 customers
customer1 = Customer(
        firstName='John',
        lastName='Doe',
        username='johndoe',
        password='password123',
        custID = '1',
        custAddress='123 Main St',
        custBalance=100.0,
        maxOwing=100.0
    )

customer2 = Customer(
        firstName='Jane',
        lastName='Smith',
        username='janesmith',
        password='mypassword',
        custID = '2',
        custAddress='456 Elm St',
        custBalance=50.0,
        maxOwing=50.0
    )


customer3 = CorporateCustomer(
        firstName='Alice',
        lastName='Johnson',
        username='alicejohnson',
        password='corporate123',
        custID = '3',
        custAddress='789 Oak St',
        custBalance=200.0,
        maxOwing=150.0,
        discountRate=0.9,  # Discount rate for corporate customer
        maxCredit=300.0,
        minBalance=100.0
    )

customer4 = CorporateCustomer(
        firstName='Bob',
        lastName='Brown',
        username='bobbrown',
        password='securepass',
        custID = '4',
        custAddress='321 Pine St',
        custBalance=500.0,
        maxOwing=200.0,
        discountRate=0.9,  # Discount rate for corporate customer
        maxCredit=600.0,
        minBalance=300.0
    )

# Insert 5 orders
order1 = Order(orderCustomer="1", orderDate="2023-01-01", orderNumber="1", orderStatus="Pending")
order2 = Order(orderCustomer="2", orderDate="2023-02-01", orderNumber="2", orderStatus="Completed")
order3 = Order(orderCustomer="3", orderDate="2023-03-01", orderNumber="3", orderStatus="Shipped")
order4 = Order(orderCustomer="4", orderDate="2023-04-01", orderNumber="4", orderStatus="Pending")
order5 = Order(orderCustomer="5", orderDate="2023-05-01", orderNumber="5", orderStatus="Cancelled")

# Insert 5 premade boxes
box1 = PremadeBox(boxSize="small", numOfBoxes=10)
box2 = PremadeBox(boxSize="medium", numOfBoxes=20)
box3 = PremadeBox(boxSize="large", numOfBoxes=30)
box4 = PremadeBox(boxSize="small", numOfBoxes=5)
box5 = PremadeBox(boxSize="medium", numOfBoxes=15)

# Insert 5 payments
payment1 = CreditCardPayment(paymentAmount=100.00, paymentDate="2023-01-02", id="1", cardExpiryDate="12/25", cardNumber="1234567890123456", cardType="credit")
payment2 = CreditCardPayment(paymentAmount=200.00, paymentDate="2023-02-02", id="2", cardExpiryDate="11/24", cardNumber="2345678901234567", cardType="credit")
payment3 = DebitCardPayment(paymentAmount=150.00, paymentDate="2023-03-02", id="3", bankName="Bank of A", debitCardNumber="3456789012345678")
payment4 = DebitCardPayment(paymentAmount=120.00, paymentDate="2023-04-02", id="4", bankName="Bank of B", debitCardNumber="4567890123456789")
payment5 = CreditCardPayment(paymentAmount=300.00, paymentDate="2023-05-02", id="5", cardExpiryDate="10/23", cardNumber="5678901234567890", cardType="credit")

# Add data to the session and commit
session.add_all([staff1, staff2, staff3, staff4, staff5,
                 customer1, customer2, customer3, customer4,
                 order1, order2, order3, order4, order5,
                 box1, box2, box3, box4, box5,
                 payment1, payment2, payment3, payment4, payment5])

session.commit()

print("Data inserted successfully!")

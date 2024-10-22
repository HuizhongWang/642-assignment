# Base class
class Person:
    def __init__(self, firstName, lastName, username, password):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.password = password

# Staff class
class Staff(Person):
    def __init__(self, firstName, lastName, username, password, dateJoined, deptName, listOfCustomers, listOfOrders, premadeBoxes, staffID, veggies):
        super().__init__(firstName, lastName, username, password)
        self.dateJoined = dateJoined
        self.deptName = deptName
        self.listOfCustomers = listOfCustomers
        self.listOfOrders = listOfOrders
        self.premadeBoxes = premadeBoxes
        self.staffID = staffID
        self.veggies = veggies

# Customer class
class Customer(Person):
    def __init__(self, firstName, lastName, username, password, custID, custAddress, custBalance, maxOwing):
        super().__init__(firstName, lastName, username, password)
        self.custID = custID
        self.custAddress = custAddress
        self.custBalance = custBalance
        self.maxOwing = maxOwing
        # self.listOfPayments = []

# CorporateCustomer class
class CorporateCustomer(Customer):
    def __init__(self, firstName, lastName, username, password, custID, custAddress, custBalance, maxOwing, discountRate, maxCredit, minBalance):
        super().__init__(firstName, lastName, username, password, custID, custAddress, custBalance, maxOwing)
        self.discountRate = discountRate
        self.maxCredit = maxCredit
        self.minBalance = minBalance

# Order class
class Order:
    def __init__(self, orderCustomer, orderDate, orderNumber, orderStatus):
        self.orderCustomer = orderCustomer
        self.orderDate = orderDate
        self.orderNumber = orderNumber
        self.orderStatus = orderStatus
        # self.listOfItems = []

# OrderLine class
class OrderLine:
    def __init__(self, itemNumber):
        self.itemNumber = itemNumber

# Item class
class Item:
    def __init__(self, itemNumber):
        self.itemNumber = itemNumber

# Veggie class
class Veggie(Item):
    def __init__(self, vegName):
        self.vegName = vegName

# WeightedVeggie class
class WeightedVeggie(Veggie):
    def __init__(self, vegName, weight, weightPerKilo):
        super().__init__(vegName)
        self.weight = weight
        self.weightPerKilo = weightPerKilo

# PackVeggie class
class PackVeggie(Veggie):
    def __init__(self, vegName, numOfPack, pricePerPack):
        super().__init__(vegName)
        self.numOfPack = numOfPack
        self.pricePerPack = pricePerPack

# UnitPriceVeggie class
class UnitPriceVeggie(Veggie):
    def __init__(self, vegName, pricePerUnit, quantity):
        super().__init__(vegName)
        self.pricePerUnit = pricePerUnit
        self.quantity = quantity

# PremadeBox class
class PremadeBox(Item):
    def __init__(self, boxSize, numOfBoxes):
        self.boxSize = boxSize
        self.numOfBoxes = numOfBoxes
        self.boxContent = []

    def BoxPrice(self):
        # Define the method to calculate box price
        pass

# Payment class
class Payment:
    def __init__(self, paymentAmount, paymentDate, paymentID):
        self.paymentAmount = paymentAmount
        self.paymentDate = paymentDate
        self.paymentID = paymentID

# CreditCardPayment class
class CreditCardPayment(Payment):
    def __init__(self, paymentAmount, paymentDate, paymentID, cardExpiryDate, cardNumber, cardType):
        super().__init__(paymentAmount, paymentDate, paymentID)
        self.cardExpiryDate = cardExpiryDate
        self.cardNumber = cardNumber
        self.cardType = cardType

# DebitCardPayment class
class DebitCardPayment(Payment):
    def __init__(self, paymentAmount, paymentDate, paymentID, bankName, debitCardNumber):
        super().__init__(paymentAmount, paymentDate, paymentID)
        self.bankName = bankName
        self.debitCardNumber = debitCardNumber

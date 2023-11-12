#!/usr/bin/env python3

#Jaocb Foppes CINF308 Progrmaing For INF Proejct 12 - Algorithyms - Stock Manager

import csv
import operator
import time
import os
import shutil
owd = os.getcwd()

""" This program reports stock of items for a warehouse
    stock levels will be pulled from and saved to a CSV file"""
    

stockRoom = [] # dictionary of procuts and stock levels 
inStock = []
onOrder = {}
prodCats = ["","phone","watch","laptop","tablet","desktop"]

res4Fullfillment = {}
owd = os.getcwd()



""" Back Of House - Processing an online order for fullfillment. 
This Program will take any number of "order" csv files as an input .
The order csv file will have a numeric name, a customer name, a cusotomer emial, and a customer phone number, and address, 
as well as the lsit of products and qualites the cusotmer is ordering.
This progrma will process the order csv file and subtract the qanitites from the instock quanity, and add them to the on order list. 
It will then generate a line in the fullfillment document 
This program will use the inventory system I created in week 10"""

# This section will process the csv files in the orders foler 
orders = [] # list of all orders each order is 
def processOrders():
    readStock()
    global stockRoom,inStock,onOrder
    print("Rrocessing Orders... ")
    incommingDir = "incomming_orders/"
    os.chdir(incommingDir)
    for file in os.listdir():# for each file in the ordere dir: read the first line 
        neworder = [] 
        with open(file) as f: # open the order csv file,read it and add the contact info to the dictionary of the new order
            order = csv.reader(f)
            custInf = list(csv.DictReader(f))
            contactInfo=custInf[0]
            neworder.append(contactInfo)
            f.close()
        with open(file) as f: # open the same order file startin g at line 3 (lines 1, 2 are the contact info )
            order = csv.reader(f)
            order = list(order)
            order = order[2:]
            cart = {}
            for i in order:
                cart[i[0]]= int(i[1]) # adding entry to cart where key is anme of item and vlaue is the qty ordered
            neworder.append(cart) # add the cart to the order withthe cusotmer info
            orders.append(neworder) # add the processed order to the end of the orders list
        for i in stockRoom: # for each item in stockroom identify key value item pairs and if the items  in the cart, subtract the number ordered for the instock qty
            for key,value in cart.items():
                if i["Product_Name"] == key:
                    i["Stock_Level"] -=value
            
        
        src = "incomming_orders/{}".format(file) #defining order file DIR
        dst = "processed_orders/{}".format(file) # defining processed order DIR
        os.chdir(owd)
        shutil.move(src,dst) # move the order from incomming to processesed
        os.chdir(incommingDir)
        print("""
            Order {num} for {name} processed
              """.format(num=neworder[0]["ORDER-ID"],name = neworder[0]["LAST"]), order)
    # save the stockroom data 
    keys = stockRoom[0]
    os.chdir(owd) 
    with open("stock.csv","w",newline="") as stocklevs: #open the Stockroom CSV and write changes to it 
                writer = csv.DictWriter(stocklevs,keys)
                writer.writeheader()
                writer.writerows(stockRoom)
                stocklevs.close()    
      
    
       
             
def readStock(): # this function read the CSV file of stock levels and creates dictionaiores of each prodcut to add to the stockroom list 
    global stockRoom,inStock,onOrder
    stockRoom = []
    inStock = []
    onOrder = {}
    os.chdir(owd)
    with open("stock.csv","r+") as s:# create lsit of products. each produt is a dictionairs 
        reader = csv.DictReader(s)
        for i in reader:
            stockRoom.append(i)
        for i in stockRoom:
            i["Stock_Level"] = int(i["Stock_Level"])
            i["Target_Stock"] = int(i["Target_Stock"])   
    for i in stockRoom: # for each key in the dict if the stock level value is >0 add the product to the inStock list 
        if i["Stock_Level"] >0:
            inStock.append(i)
    inStock = sorted(inStock, key=operator.itemgetter("Product_Name")) # sort the lsit alphabetically 

def checkStock(): # this fucntion check the instock levels vs the target stock levels and outputs a list of things that need to be ordered and how many need to be ordered 
    global onOrder
    for i in stockRoom: # for each dixtioanry in the list of stockroom dictionaies 
        if i["Stock_Level"] < i["Target_Stock"]: # if the instock quantity is less than that target stock, add the item to the onOrder lsit wit hthe number we need to order
            need = i["Target_Stock"] - i["Stock_Level"]
            onOrder[i["Product_Name"]] = need # create list of procut names and the numbe rthat needs to be ordered 
    onOrder = dict(reversed(sorted(onOrder.items(), key=operator.itemgetter(1)))) # sort dict based on numer that needs to be ordered 
    print("\nWe need to order the following products\n",onOrder) # this returns          
    time.sleep(1)
    stockLevel()
    
def inStockByCat():# this func takes a category as an input and output a list of produts in stock in that category
    allCats = []
    for i in inStock:
        if i["Product_Category"] not in allCats:
            allCats.append(i["Product_Category"])
    cat = input("""
                Which Category Would you like to view
                {Categories}
                """.format(Categories=allCats))
    for i in inStock:
        if i["Product_Category"]== cat:
            print(i["Product_Name"]+":",i["Stock_Level"],"in stock")
    time.sleep(1)
    stockLevel()
def outOfStock(): # this function checs for items that are out of stock 
    ooStock = []
    for i in stockRoom:
        if i["Stock_Level"] < 1:
            ooStock.append(i)
    print('''
          The Following Items are out of stock:
    ''')
    for i in ooStock:
        print(i["Product_Name"]+": "+str(i["Stock_Level"])+ " on hand")
    time.sleep(2)
    stockLevel()
            

def stockLevel(): #This fuction will show stock level of all products or a requested product
    choice = int(input("""
                   How would you like to view stock?
                   (1) for All In Stock Products
                   (2) to choose a specific Product Category
                   (3) to see items running low
                   (4) to View Out of Stock Items
                   (5) to exit
                   """))
    if choice == 1:
        print("\n\nWe have the following items in stock: \n")
        for i in inStock:
            print(i["Product_Name"]+":",i["Stock_Level"],"on hand")
        stockLevel()
    elif choice == 2:
        inStockByCat()
    elif choice == 3:
        checkStock()
    elif choice == 4:
        outOfStock()
    elif choice == 5:
        welcome()
    else:
        print("""
              Please Choose an avaible option""")
        stockLevel()

def newProduct(prodType): # this fuction will allow a user to define a enw prodcut with a name, product category, and stock level 
    
    newThing = {}
    newThing["Product_Name"]= input("""
                                    Enter the Product Name:
                                    """)
    newThing["Product_Category"]= prodType
    
    try:
        newThing["Stock_Level"]= int(input("""
                                    Enter the current Stock Level:
                                    """))
    except:
        print("Stock level must be an integer. Try again ")
    try:
        newThing["Target_Stock"]= int(input("""
                                    Enter the Target Stock Level:
                                    """))
    except:
        print("Stock level must be an integer. Try again ")
        

    with open("stock.csv","a",newline="") as stocklevs: #open player wokedex file 
        writer = csv.DictWriter(stocklevs,fieldnames=newThing.keys())
        writer.writerow(newThing)
        stocklevs.close()

def incommingShipment(prodType): # this fuction will allow a user to update/increment stock levels 
    newTotal = 0  
    recievingTypes = [] # list of products within the 
    for i in stockRoom:
        if i["Product_Category"] == prodType: #if product catagorys is the slected prouct type add it to a list of poducts avaible to recice 
            recievingTypes.append(i["Product_Name"]) 
    choice = input("""
                   Which Product are you recieving:
                   {Prods}""".format(Prods=recievingTypes))
    if choice not in recievingTypes:
        print("Please make a valid choice")
        incommingShipment(prodType)
    else:
        try:
            ammount = int(input("""
                                How many are you recieving?
                                """))
        
            for i in stockRoom:
                if i["Product_Name"] == choice:
                    i["Stock_Level"] +=ammount
                    newTotal = i["Stock_Level"]
            print("""Input Succesfull:
                {name}: {amount} on hand
                """.format(name=choice,amount=newTotal))
            keys = stockRoom[0]
            with open("stock.csv","w",newline="") as stocklevs: #open the Stockroom CSV and write changes to it 
                writer = csv.DictWriter(stocklevs,keys)
                writer.writeheader()
                writer.writerows(stockRoom)
                stocklevs.close()
        except:
            print("Please enter a valid number")
            time.sleep(1)
            incommingShipment()

def deleteProduct(): #This fuction will allow a user to delete a product they no longer sell 
    print("""
          All Products:""")
    allItems = [] # lsit of all itme names currently in stock room list 
    for i in stockRoom:
        print("""{}""".format(i["Product_Name"]))
        allItems.append(i["Product_Name"])
    choice = input("""
                   Enter the Name of the product you would like to delete
                   """)
    if choice in allItems:
        for i in stockRoom:
            if i["Product_Name"] == choice:
                stockRoom.remove(i)
                print("Removed ",choice,"from stockroom ")
        print(stockRoom)
        keys = stockRoom[0]
        with open("stock.csv","w",newline="") as stocklevs: #open the Stockroom CSV and write changes to it 
                writer = csv.DictWriter(stocklevs,keys)
                writer.writeheader()
                writer.writerows(stockRoom)
                stocklevs.close()
    else:
        print("Please enter a valid choice")
        deleteProduct()

def welcome(): # This fuction is where the user will be able to choose what they want to do 
    readStock()
    choice = int(input("""
                   ***Welcome to Inventory Controll***
                   
                   Enter (1) to View Product Stock
                   
                   Enter (2) to Input incomming Shipment Data
                   
                   Enter (3) to Create a new Product
                   
                   Enter (4) to Delete a Product
                   
                   Enter (5) To Process orders
                   """))
    if choice == 1:
        stockLevel()
    elif choice == 2:
        prodType = int(input("""
                       Choose a product category:
                       (1) Phone
                       (2) Watch
                       (3) Laptop
                       (4) Tablet
                       (5) Desktop
                       (6) to go back
                       
                       """))
        if prodType == 1 or 2 or 3 or 4 or 5:
            incommingShipment(prodCats[prodType]) # run incomming shoipmetn fucntion for slected product category type 
        elif prodType == 6:
            welcome()
        else:
            print("Make a valid choice")  
    elif choice == 3:
        prodType = int(input("""
          What Product Type would you like to add to the catalog?
          (1) Phone
          (2) Watch
          (3) Laptop
          (4) Tablet
          (5) Desktop
          (6) to go back 
          """))
        if prodType == 1 or 2 or 3 or 4 or 5:
            newProduct(prodCats[prodType])# run new product funct for selesfted product type 
        elif prodType == 6:
            welcome()
        else:
            print("Make a valid choice")  
    elif choice == 4:
        deleteProduct()
    elif choice == 5:
        processOrders()
while True:
    welcome() 
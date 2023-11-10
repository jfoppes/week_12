#!/usr/bin/env python3
# Foppes, Jacob Algorithms Discussion Post

''' A Stock room has several product that it keeps on hand. They need to be able to see whcih products are in stock and what needs to be ordered. '''

stockRoom = {"watch":7,"iphone":10,"macbook":4,"ipad":5,"pencil":0,"wband":0} # dictionary of procuts and stock levels 
targetStock = {"watch":10,"iphone":15,"macbook":6,"ipad":5,"pencil":4,"wband":10} #dictionary or products and thier target stock 
inStock = []
onOrder = {}
def weGotIt(): # this fuction determines what products are instock 
    global inStock
    for i in stockRoom.keys(): # for each key in the dict if the stock level value is >0 add the product to the inStock list 
        if stockRoom[i] >0:
            inStock.append(i)
    inStock = sorted(inStock) # sort the lsit alphabetically       
    print("\n\nWe have the following items in stock: \n",inStock)     
      
weGotIt() # This returns ['ipad', 'iphone', 'macbook', 'watch'], as those are the only products in stock at this time 


def checkStock(): # this fucntion check the instock levels vs the target stock levels and outputs a list of things that need to be ordered and how many need to be ordered 
    global onOrder
    for key,value in stockRoom.items(): # for each item in the stock list compare its value to the correponsidng item in the TargetStock list 
        for key,value in targetStock.items():
            if stockRoom[key] < targetStock[key]: # if the instock quantity is less than that target stock, add the item to the onOrder lsit wit hthe number we need to order
                need = targetStock[key] - stockRoom[key]
                onOrder[key] = need
    print(onOrder) # this returns {'watch': 3, 'iphone': 5, 'macbook': 2, 'pencil': 4, 'wband': 10} as we need 1o watches but only ahve 7, need 15 phones but only ahve 10 etc           
checkStock()
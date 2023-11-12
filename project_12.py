#!/usr/bin/env python3

import csv
import os
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
    incommingDir = "incomming_orders/"
    os.chdir(incommingDir)
    for file in os.listdir():# for each file in the ordere dir: read the first line 
        neworder = [] 
        with open(file) as f:
            order = csv.reader(f)
            custInf = list(csv.DictReader(f))
            contactInfo=custInf[0]
            neworder.append(contactInfo)
            f.close()
        with open(file) as f:
            order = csv.reader(f)
            order = list(order)
            order = order[2:]
            cart = {}
            for i in order:
                cart[i[0]]= int(i[1])
            neworder.append(cart)
            orders.append(neworder)
        src = "incomming_orders/{}".format(file)
        dst = "processed_orders/{}".format(file)
        print("""
            Order {num} for {name} processed
              """.format(num=neworder[0]["ORDER-ID"],name = neworder[0]["LAST"]))
       # os.chdir(owd)
       # shutil.move(src,dst)
       # os.chdir(incommingDir)
    
    
processOrders()
for i in orders:
    print("\n\n",i)
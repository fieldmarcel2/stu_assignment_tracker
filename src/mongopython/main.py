
# bank account
# 1.deposit
# 2. withdraw
# 3. get_balance()
# when u u create the object of a bank account it is mapped to a specific user any

from pymongo import MongoClient

import json


from flask import Flask,request

app= Flask(__name__)

MONGO_URI = "mongodb+srv://tripathi20t_db_user:YcvNRnPnxRs1w1Jr@attendanceassign.sbapwws.mongodb.net/"

client= MongoClient(MONGO_URI)

db= client["bankacc"]
collection= db["bankacc1"]


print("connected")

class bankAccount:
 def __init__(self,id,name,balance =0):
  self.id=id
  self.name= name
  self.balance= balance

  user =  collection.find_one({"id":id})
  if user:
            self.balance = user["balance"]
  else:
            self.balance = 0

            collection.insert_one({
                "id":id,
                "name": name,
                "balance": balance
            })



 def deposit(self,new_amount:float):
    user = collection.find_one({"id":self.id})
    new_balance = user["balance"] + new_amount

    if user["balance"] >=0:
     collection.update_one(
    {"id": self.id},
    {"$set": {"balance": new_balance}}
     )

    self.balance = new_balance

 def withdraw(self,withdraw_amount:float):
       user = collection.find_one({"id":self.id})
       
       if  withdraw_amount >=0:
          if user["balance"]-withdraw_amount   <0:
               print("insufficient balance")

          else :  
               new_balance = user["balance"] - withdraw_amount

               collection.update_one(
                {"id": self.id},
                {"$set": {"balance": new_balance}}
            )

               self.balance = new_balance

               print(f"{withdraw_amount} is withdrawn") 

 def get_bal(self):
        user = collection.find_one({"id": self.id})

        self.balance = user["balance"]

        print(f"{self.balance} is balance")

        return self.balance


p1 = bankAccount(3, "tripathi", 10000)

p1.deposit(50)

p1.withdraw(20)

p1.get_bal()
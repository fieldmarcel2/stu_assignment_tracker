#create a flask api that contains one endpoint called /search 
# thsi receives a query param that is search keyword  
# search this keyword in both first and last namem and resturn list of items
# deo not retrive the entiredata 
# .'find a way to retieve data from db '



from pymongo import MongoClient

import json

from flask import Flask,request

app= Flask(__name__)

MONGO_URI = "mongodb+srv://tripathi20t_db_user:YcvNRnPnxRs1w1Jr@attendanceassign.sbapwws.mongodb.net/"


client= MongoClient(MONGO_URI)

db= client["mongopython"]
collection= db["mongopython1"]


print( "connected")

with open ("../../MOCK_DATA.json") as file:
    data= json.load(file)


collection.insert_many(data)    
print("data inserted")

@app.get("/search")

def search():
    keyword = request.args.get("keyword","")

    result= collection.find( {

        "$or": [

            {"first_name":{ "$regex" :keyword , "$options":"i"}},
            {"last_name":{ "$regex" :keyword , "$options":"i"}}
        ]
    })


    userdata= list(result)
    userdata = list( map( lambda x: {**x, "_id":str(x["_id"])},userdata))
    return userdata

if __name__== "__main__":
    app.run(debug= True)

# x= collection.find_one({"id":1})
# print(x)


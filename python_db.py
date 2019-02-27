import pymongo
import hashlib
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["coffeeHouse"]
print(mydb.list_collection_names())
user = mydb["userschemas"]
shop = mydb["shopschemas"]

shopA = {
    "shop_id" : "shA",
    "shop_name" : "shopA",
    "shop_pass" : hashlib.md5("passwd".encode('utf-8')).hexdigest(),
    "mail" : "shop.A@mail.com",
    "openTime" : 80,
    "closeTime" : 200,
    "location" :  {
        "Longitude": 23,
        "Latitude": 44
    },
    "address" : "SF Bay"
}
shopB = {
    "shop_id" : "shB",
    "shop_name" : "shopB",
    "shop_pass" : hashlib.md5("passwd".encode('utf-8')).hexdigest(),
    "mail" : "shop.B@mail.com",
    "openTime" : 80,
    "closeTime" : 200,
    "location" :  {
        "Longitude": 23,
        "Latitude": 44
    },
    "address" : "Marine Drive"
}
shopC = {
    "shop_id" : "shC",
    "shop_name" : "shopC",
    "shop_pass" : hashlib.md5("passwd".encode('utf-8')).hexdigest(),
    "mail" : "shop.C@mail.com",
    "openTime" : 80,
    "closeTime" : 200,
    "location" :  {
        "Longitude": 23,
        "Latitude": 44
    },
    "address" : "Kannan Street"
}
shopD = {
    "shop_id" : "shD",
    "shop_name" : "shopD",
    "shop_pass" : hashlib.md5("passwd".encode('utf-8')).hexdigest(),
    "mail" : "shop.D@mail.com",
    "openTime" : 80,
    "closeTime" : 200,
    "location" :  {
        "Longitude": 23,
        "Latitude": 44
    },
    "address" : "Rajesh Residency"
}
custa = {
   "username" : "cust1",
   "name" :  "CustomerA",
   "email" : "custA@mail.com",
   "passwd" : hashlib.md5("passwd".encode('utf-8')).hexdigest()
}

custb = {
   "username" : "cust2",
   "name" :  "CustomerB",
   "email" : "custB@mail.com",
   "passwd" : hashlib.md5("passwd".encode('utf-8')).hexdigest()
}
custc = {
   "username" : "cust3",
   "name" :  "CustomerC",
   "email" : "custC@mail.com",
   "passwd" : hashlib.md5("passwd".encode('utf-8')).hexdigest()
}
custD = {
   "username" : "cust4",
   "name" :  "CustomerD",
   "email" : "custD@mail.com",
   "passwd" : hashlib.md5("passwd".encode('utf-8')).hexdigest()
}
custE = {
   "username" : "cust5",
   "name" :  "CustomerE",
   "email" : "custE@mail.com",
   "passwd" : hashlib.md5("passwd".encode('utf-8')).hexdigest()
}
custF = {
   "username" : "cust6",
   "name" :  "CustomerF",
   "email" : "custF@mail.com",
   "passwd" : hashlib.md5("passwd".encode('utf-8')).hexdigest()
}
custG = {
   "username" : "cust7",
   "name" :  "CustomerG",
   "email" : "custG@mail.com",
   "passwd" : hashlib.md5("passwd".encode('utf-8')).hexdigest()
}

x = [custa,custb,custc,custD,custE,custF,custG]
user.insert_many(x)
x = [shopA,shopB,shopC,shopD]
shop.insert_many(x)
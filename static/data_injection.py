import pymongo
import random

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["coffeeHouse"]
print(db.list_collection_names())
col = db["reviews"]
col1 = db["userschemas"]
col2 = db["shopschemas"]

ss = []
for i in col1.find():
    for j in col2.find():
        mydict = {
            "userId": i["username"],
            "shopId": j["shop_id"],
            "rating": random.randint(-1, 5)
        }
        ss.append(mydict)

col.insert_many(ss)

# food_list=[]
# foods=[]
# x=col2.find()
# foodItem = ['burger','pizza','latte','mocha','capuccino','pasta','bhatoore','moose','cheesecake'];
# for i in x:
#     print(i["food_name"])
#     food = {"food_name":i}
#     col2.insert_one(food)
#
# shops = []
# x = col3.find()

# for i in x:
#     for j in range(4):
#         mydict = {
#             "shopId": i['shop_id'],
#             "food_name": random.choice(foodItem),
#             "costPerUnit" : random.randint(10,100)
#         }
#         print(mydict)
#         shops.append(mydict)
#     # print(mydict)
#
# print(col.insert_many(shops).inserted_ids)

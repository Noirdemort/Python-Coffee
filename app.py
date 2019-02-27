from flask import Flask, render_template, request, url_for,jsonify, redirect
import pymongo
import random
import hashlib
from bson.objectid import ObjectId
import pytz
from datetime import datetime


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["coffeeHouse"]

app = Flask(__name__)


def hasher(aa):
    aa = hashlib.md5(aa.encode("utf-8")).hexdigest()
    return aa


@app.route('/', methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/userlogin.html', methods=["GET"])
def user_login():
    return render_template("userlogin.html")


@app.route("/shoplogin.html", methods=["GET", "POST"])
def shop_login():
    return render_template("shoplogin.html")


@app.route("/usersignup.html", methods=["GET", "POST"])
def serve_page():
    return render_template("usersignup.html")


@app.route("/shop_register.html", methods=["GET", "POST"])
def regme():
    return render_template("shop_register.html")


@app.route("/user_log", methods=["GET", "POST"])
def user_log():
    data = dict(request.form)
    print(data)
    username = data["uname"][0]
    myquery = {"username": username}
    col = db["userschemas"]
    x = col.find_one(myquery)
    if x is not None:
        if x["passwd"] == hasher(data["password"][0]):
            return render_template("main.html", name=x["name"], id=x["username"])
        elif x["passwd"] != hasher(data["password"][0]):
            return "<HTML><head><title>Error</title></head><body> <h1>Oops! Wrong password! </h1></body></HTML>"
    else:
        return "<HTML><head><title>Error</title></head><body> <h1>Account not found! </h1></body></HTML>"


@app.route("/shop_log", methods=["GET", "POST"])
def shop_log():
    data = dict(request.form)
    username = data["shopname"][0]
    myquery = {"shop_id": username}
    col = db["shopschemas"]
    x = col.find_one(myquery)
    if x is not None:
        if x["shop_pass"] == hasher(data["password"][0]):
            # find orders
            # find reviews
            col2 = db["reviews"]
            col2 = col2.find({"shopId": x["shop_id"]}).limit(7)
            reviews = []
            orders = {}

            col3 = db["orderschemas"]
            col3 = col3.find({"shopId": x["shop_id"]})
            colOrders = db["orderschemas"]
            colOrders = colOrders.find({"shopId": x["shop_id"]})
            col4 = db["userschemas"]
            col5 = db["menuschemas"]

            # get reviews from user
            review_count=0
            count=0
            for i in col2:
                user = col4.find_one({"username": i["userId"]})["username"]
                if int(i['rating']) != -1:
                    mydict = {
                        "username": user,
                        "rating": i["rating"]
                    }
                    count+=1
                    review_count += int(i['rating'])
                    reviews.append(mydict)
            avg_reviews = review_count/count

            # get ratings
            for i in col3:
                orders[i['uid']] = []

            total_cost = {}
            food_prices = db["menudistschemas"]
            for i in colOrders:
                myquery = {"food_name": i["food_name"], "shopId": x['shop_id']}
                food_price = int(food_prices.find_one(myquery)['costPerUnit'])
                orders[i['uid']].append(tuple((i['food_name'], i['amount'], food_price)))

            for user in orders:
                total = 0
                for i in orders[user]:
                    myquery = {"food_name": i[0], "shopId": x['shop_id']}
                    food_price = int(food_prices.find_one(myquery)['costPerUnit'])
                    total += food_price*int(i[1])
                total_cost[user] = total

            return render_template("shop_main.html", name=x['shop_name'], shop_id=x['shop_id'], reviews=reviews, orders=orders, expense=total_cost, avg_review=round(avg_reviews,2))

        elif x["shop_pass"] != hasher(data["password"][0]):
            return "<HTML><head><title>Error</title></head><body> <h1>Oops! Wrong password! </h1></body></HTML>"
    else:
        return "<HTML><head><title>Error</title></head><body> <h1>Account not found! </h1></body></HTML>"


@app.route("/user_register", methods=["GET", "POST"])
def register():
    data = dict(request.form)
    mydict = {
        "username": data['sigUname'][0],
        "name": data['sigName'][0],
        "email": data['sigEmail'][0],
        "passwd": hasher(data['sigPass'][0])
    }
    jerry = {"username": data['sigUname'][0]}
    col = db["userschemas"]
    x = col.find_one(jerry)
    if x is None:
        col.insert_one(mydict)
        print("User successfully created!")
        return redirect("userlogin.html")
    else:
        return "<HTML><head><title>Error</title></head><body> <h1>Username already exists! </h1></body></HTML>"


@app.route("/shop_signup", methods=["GET", "POST"])
def shop_register():
    data = dict(request.form)
    mydict = {
    "shop_id": data['id'][0],
    "shop_name": data['sname'][0],
    "shop_pass": hasher(data['spass'][0]),
    "mail": data['email'][0],
    "openTime": data['opentime'][0],
    "closeTime": data['closetime'][0],
    "location":  {
                       "Longitude": int(data['longitude'][0]),
                       "Latitude": int(data['lattitude'][0])
               },
    "address": data['address'][0]
}
    jerry = {"shop_id": data['id'][0]}
    col = db["shopschemas"]
    x = col.find_one(jerry)
    if x is None:
        col.insert_one(mydict)
        print("Shop successfully created!")
        return redirect("/shoplogin.html")
    else:
        return "<HTML><head><title>Error</title></head><body> <h1>Shop-ID already exists! </h1></body></HTML>"


@app.route("/nearest", methods=["GET", "POST"])
def get_nearest():
    a = random.randint(1, 15)
    b = random.randint(1, 15)
    data = dict(request.form)
    print(data)
    username = data['username'][0]
    col = db["shopschemas"]
    x = col.find()
    metaDataArray = []
    distanceArray = []
    for i in x:
        dist = abs(i["location"]["Latitude"]-a) + abs(i["location"]["Longitude"]-b)
        distanceArray.append(dist)
        metaDataArray.append(i)

    for i in range(len(distanceArray)):
        for j in range(len(distanceArray)):
         if distanceArray[i] > distanceArray[j]:
            temp = distanceArray[i]
            distanceArray[i] = distanceArray[j]
            distanceArray[j] = temp
            temp = metaDataArray[i]
            metaDataArray[i] = metaDataArray[j]
            metaDataArray[j] = temp

    return render_template("shop_list.html", shops=metaDataArray, by=username)


@app.route("/best", methods=["GET", "POST"])
def get_best():
    data = dict(request.form)
    print(data)
    username = data['username'][0]
    col = db['reviews']
    print(list(col.find()))
    best = list(col.group(["shopId"], {}, {"count": 0}, "function(o, p){p.count++}" ))
    shop_rates = {}
    for i in best:
        print(i)
        shop_rates[i['shopId']] = i['count']

    sorted_by_value = sorted(shop_rates.items(), key=lambda kv: kv[1])
    shops = []
    tel = db['shopschemas']
    for i in sorted_by_value:
        shop = tel.find_one({"shop_id": i[0]})
        shops.append(shop)
    return render_template("shop_list.html", shops=shops, by=username)


@app.route("/diversity", methods=["GET", "POST"])
def get_diversity():
    data = dict(request.form)
    print(data)
    col = db["menudistschemas"]
    username = data['username'][0]
    # pipe = [{'$group': {'_id': '$shopId', 'count' : { '$sum':1 }}}]
    diversity = list(col.group(["shopId"], {}, {"count":0},"function(o, p){p.count++}" ))
    print(diversity)
    food_length = {}
    shops = []

    for i in diversity:
        print(i)
        food_length[i['shopId']] = i['count']

    sorted_by_value = sorted(food_length.items(), key=lambda kv: kv[1])

    tel = db['shopschemas']
    for i in sorted_by_value:
        shop = tel.find_one({"shop_id": i[0]})
        shops.append(shop)

    return render_template("shop_list.html", shops=shops, by=username)


@app.route("/shopmenu.html", methods=["GET", "POST"])
def regA():
    data = dict(request.form)
    shop_id = data['shop_id'][0]
    col = db["menuschemas"]
    foods = col.find()
    food_list = []
    for i in foods:
        food_list.append(i['food_name'])
    return render_template("shop_menu.html", food_items=food_list, by=shop_id)


@app.route("/logout", methods=["GET", "POST"])
def rift():
    return redirect("/index.html")


@app.route("/add_food", methods=["GET", "POST"])
def add_food():
    data = dict(request.form)
    print(data)
    col0 = db["menudistschemas"]
    col2 = db["menuschemas"]

    if "special" in data.keys():
        food = data['special'][0]
        by = data['shop_id']
        at = data['price'][0]
        mydict = {
            "shopId": by,
            "food_name": food,
            "costPerUnit": at
        }
        adder = {"food_name": food}
        col0.insert_one(mydict)
        col2.insert_one(adder)
    else:
        foods = data['fooz']
        by = data['shop_id']
        at = data['price']
        z = []
        for i in foods:
            mydict = {
                "shopId": by,
                "food_name": i,
                "costPerUnit": at[foods.index(i)]
            }
            z.append(mydict)
        col0.insert_many(z)
    return redirect("/shoplogin.html")



@app.route("/return_main_user", methods=["GET", "POST"])
def getBack():
    data = dict(request.form)
    print(data)
    username = data['username'][0]
    myquery = {"username": username}
    col = db["userschemas"]
    x = col.find_one(myquery)
    return render_template("main.html", name=x["name"], id=x["username"])


@app.route("/order_food", methods=["GET", "POST"])
def order_food():
    data = dict(request.form)
    print(data)
    username = data['username'][0]
    shop_id = data['shop_id'][0]
    col = db["menudistschemas"]
    my_query = {"shopId": shop_id}
    x = col.find(my_query)
    food_prep = []
    for i in x:
        food_prep.append(tuple((i["food_name"], i['costPerUnit'])))
    return render_template("order.html", by=username, at=shop_id, foods=food_prep)


@app.route("/place_order", methods=["GET", "POST"])
def place_order():
    data = dict(request.form)
    print(data)
    username = data['username'][0]
    shop_id = data['shop_id'][0]
    foods = data['items']
    amount = data['quantity']
    col = db['orderschemas']
    add = []
    for i in range(len(foods)):
        if int(amount[i])>0:
            mydict = {
                "uid":username,
                "shopId":shop_id,
                "food_name": foods[i],
                "amount": amount[i],
                "transaction_date": datetime.now(pytz.utc)
            }
            print(mydict)
            add.append(mydict)
    print(add)
    col.insert_many(add)
    print("orders created successfully.")
    z = db['userschemas']
    iser = z.find_one({"username": username})
    return render_template("main.html",name=iser['name'],id=username)


if __name__ == '__main__':
    app.run(debug=True)

# This program will generate traffic for ACME Fitness Shop app. It simulates both
# Authenticated and Guest user scenarios. You can run this program either from
# command line or from the web based UI. Refer to the "locust" documentation for
# further information. 

import logging
import random
from locust import HttpUser, TaskSet, task, SequentialTaskSet


# List of users (pre-loaded into ACME Fitness shop)
users = ["eric", "phoebe", "dwight", "han"] 

# List of products within the catalog
products = []


# GuestUserBrowsing simulates traffic for a Guest User (Not logged in)
class GuestUserBrowsing(SequentialTaskSet):

    def on_start(self):
        self.getProducts()

    def listCatalogItems(self):
        items = self.client.get("/products").json()["data"]
        for item in items:
            products.append(item["id"])
        return products

    @task(1)
    def getProducts(self):
        logging.info("Guest User - Get Products")
        self.client.get("/products")

    @task(2)
    def getProduct(self):
        logging.info("Guest User - Get a product")
        products = self.listCatalogItems()
        product_id = random.choice(products)
        product = self.client.get("/products/"+ product_id).json()
        logging.info("Product info - " +  str(product))
        products.clear()


# AuthUserBrowsing simulates traffic for Authenticated Users (Logged in)
class AuthUserBrowsing(SequentialTaskSet):

    def on_start(self):
        self.login()

    @task(1)
    def login(self):
        user = random.choice(users)
        logging.info("Auth User - Login user " + user)
        body = self.client.post("/login/", json={"username": user, "password":"vmware1!"}).json()
        self.user.userid = body["token"]

    @task(1)
    def getProducts(self):
        logging.info("Auth User - Get Catalog")
        self.client.get("/products")

    @task(2)
    def getProduct(self):
        logging.info("Auth User - Get a product")
        products = self.listCatalogItems()
        product_id = random.choice(products)
        product = self.client.get("/products/"+ product_id).json()
        logging.info("Product info - " +  str(product))
        products.clear()

    @task(2)
    def addToCart(self):
        self.listCatalogItems()
        productid = random.choice(products)
        logging.info("Add to Cart for user " + self.user.userid)
        self.client.post("/cart/item/add/" + self.user.userid, json={
                  "name": productid,
                  "price": "100",
                  "shortDescription": "Test add to cart",
                  "quantity": random.randint(1,2),
                  "itemid": productid
                })
        products.clear()

    @task(1)
    def checkout(self):
        self.client.get("/cart/items/" + self.user.userid).json()
        self.client.post("/order/add/"+ self.user.userid, json={ "userid":"8888",
                "firstname":"Eric",
                "lastname": "Cartman",
                "address":{
                    "street":"20 Riding Lane Av",
                    "city":"San Francisco",
                    "zip":"10201",
                    "state": "CA",
                    "country":"USA"},
                "email":"jblaze@marvel.com",
                "delivery":"UPS/FEDEX",
                "card":{
                    "type":"amex/visa/mastercard/bahubali",
                    "number":"349834797981", 
                    "expMonth":"12",
                    "expYear": "2022",
                    "ccv":"123"
                },
                "cart":[
                    {"id":"1234", "description":"redpants", "quantity":"1", "price":"4"},
                    {"id":"5678", "description":"bluepants", "quantity":"1", "price":"4"}
                ],
                "total":"100"})

    def listCatalogItems(self):
        items = self.client.get("/products").json()["data"]
        for item in items:
            products.append(item["id"])
        return products

    @task(2)
    def index(self):
        self.client.get("/")


class UserBehavior(TaskSet):
    tasks = {AuthUserBrowsing:2, GuestUserBrowsing:1}


class WebSiteUser(HttpUser):
    tasks = [UserBehavior]
    userid = ""
    min_wait = 2000
    max_wait = 10000

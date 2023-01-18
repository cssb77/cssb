from init_data import *
import pymongo

client = pymongo.MongoClient()
db_pet = client['pet']
c_dog = db_pet['dog']

c_dog.insert_one(d1)
c_dog.insert_one(d2)
c_dog.insert_one(d3)
c_dog.insert_one(d4)
c_dog.insert_one(d5)
c_dog.insert_one(d6)
c_dog.insert_one(d7)
c_dog.insert_one(d8)

# 【提示1】使用insert_one()方法，向数据库中添加字典数据d9
# 【提示1】使用insert_one()方法，向数据库中添加字典数据d10

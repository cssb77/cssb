import pymongo

client = pymongo.MongoClient()
db_pet = client['pet']
c_dog = db_pet['dog']

# 【提示2】使用find()方法获取所有数据，并赋值给变量res
# 【提示2】遍历res，输出所有数据

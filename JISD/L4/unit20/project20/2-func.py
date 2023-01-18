import pymongo

def dog_find(data):
    client = pymongo.MongoClient()
    db_pet = client['pet']
    c_dog = db_pet['dog']
    dog_list = []
    res = c_dog.find(data)
    for i in res:
        dog_list.append(i)
    return dog_list

# 【提示2】使用函数dog_find()查询数据库中的所有数据（传入参数{}），并保存为dog_list
dog_list = dog_find({})
# 【提示2】输出列表dog_list
print(dog_list)
# 【提示2】使用函数dog_find()查询排名为1宠物狗的数据（传入参数{'num':'1'}），并保存为dog_list
dog_list=dog_find({'num':'1'})
# 【提示2】输出列表dog_list
print(dog_list)
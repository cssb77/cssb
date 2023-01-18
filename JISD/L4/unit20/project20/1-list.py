# 想要实现在页面中显示数据，需要保存数据
# 定义空列表，向空列表中保存查询的数据

import pymongo

client = pymongo.MongoClient()
db_pet = client['pet']
c_dog = db_pet['dog']

# 【提示1】定义空列表dog_list
dog_list = []
res = c_dog.find({})
for i in res:
    # 【提示1】使用append()方法，向列表中追加字典数据i
    res.append(i)
# 【提示1】输出列表dog_list
print(dog_list)



import pymongo
import ybc_box

client = pymongo.MongoClient()
db_pet = client['pet']
c_dog = db_pet['dog']

# 【提示5】使用msgbox()方法展示所有数据和对应图片
# 【提示5】在指定位置填写msgbox()方法，并传入对应参数（数据字典i及图片位置i['img']）
res = c_dog.find({})
for i in res:
    000000
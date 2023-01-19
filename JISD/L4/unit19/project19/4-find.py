import pymongo

client = pymongo.MongoClient()
db_pet = client['pet']
c_dog = db_pet['dog']

# 【提示4】使用find()方法获取姓名为阿尔法、且品种为边境牧羊犬的狗狗数据，并输出
# 【提示4】在指定位置填写条件{'name':'阿尔法','species':'边境牧羊犬'}
res = c_dog.find(00000)
for i in res:
    print(i)

print('*-------------------------------*')

# 【提示4】使用find()方法获取所有数据，并输出
# 【提示4】在指定位置填写条件{}
res = c_dog.find(00000)
for i in res:
    print(i)
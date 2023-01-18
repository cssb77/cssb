import pymongo


# 定义函数：增加家庭成员
def family_insert(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_family = db_ybc['family']
    c_family.insert_one(data)


# 家庭成员数据
data1 = {'name': '猿爸爸','age': '42','info': '我有两个可爱的孩子','image': 'static/images/dad.png'}
data2 = {'name': '猿妈妈','age': '41','info': '我最近喜欢插花','image': 'static/images/mum.png'}
data3 = {'name': '壮猿','age': '10','info': '爱生活，爱编程','image': 'static/images/yuan.png'}
data4 = {'name': '猿小花','age': '8','info': '我喜欢吃甜甜圈','image': 'static/images/hua.png'}
data5 = {'name': '猿爷爷','age': '65','info': '钓鱼真有趣儿','image': 'static/images/grandpa.png'}
data6 = {'name': '猿奶奶','age': '65','info': '我在老年大学认识了很多朋友','image': 'static/images/grandma.png'}

family_insert(data1)
family_insert(data2)
# 【提示3】使用family_insert函数
#         将家庭成员数据增加到数据库
00000



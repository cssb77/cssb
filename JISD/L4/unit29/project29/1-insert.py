import pymongo
import uuid


# 函数：增加“”“”"小猿"账号
def user_insert():
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_user = db_ybc['user']
    user_data = {'username': '小猿', 'pwd': '123456'}
    c_user.insert_one(user_data)


# 使用函数，将小猿账号增加到数据库中
user_insert()


# 创建任务数据(字典)
todo1 = {'_id': str(uuid.uuid1()), 'username': '小猿', 'state': '未完成', 'subject': '英语', 'content': '背诵1篇文章', 'date': '2021-04-13'}
todo2 = {'_id': str(uuid.uuid1()), 'username': '小猿', 'state': '已完成', 'subject': '数学', 'content': '完成1张卷子', 'date': '2021-04-14'}
todo3 = {'_id': str(uuid.uuid1()), 'username': '小猿', 'state': '未完成', 'subject': '编程', 'content': '开发《任务本》项目', 'date': '2021-04-12'}
todo4 = {'_id': str(uuid.uuid1()), 'username': '小猿', 'state': '未完成', 'subject': '语文', 'content': '默写3首古诗', 'date': '2021-04-15'}
todo5 = {'_id': str(uuid.uuid1()), 'username': '小猿', 'state': '已删除', 'subject': '英语', 'content': '听写第一节课单词', 'date': '2021-04-13'}
todo6 = {'_id': str(uuid.uuid1()), 'username': '小猿', 'state': '已完成', 'subject': '数学', 'content': '做10道应用题', 'date': '2021-04-13'}
todo7 = {'_id': str(uuid.uuid1()), 'username': '小猿', 'state': '未完成', 'subject': '编程', 'content': '完成《在线翻译》项目', 'date': '2021-04-16'}
todo8 = {'_id': str(uuid.uuid1()), 'username': '小猿', 'state': '已完成', 'subject': '英语', 'content': '做100000000000篇阅读理解', 'date': '2021-04-14'}


# 函数：增加新的任务
def todo_insert(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_todo = db_ybc['todo']
    c_todo.insert_one(data)


# 使用函数todo_insert()，将任务数据添加到集合c_todo中
todo_insert(todo1)
todo_insert(todo2)
todo_insert(todo3)
todo_insert(todo4)
todo_insert(todo5)
todo_insert(todo6)
todo_insert(todo7)
todo_insert(todo8)


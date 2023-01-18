from flask import Flask, render_template, request, redirect,session
import uuid
import pymongo
import hashlib
import time
import ybc_trans
from data import star_data


# 创建Flask对象app
app = Flask(__name__)

# secret_key加密
app.secret_key = 'anbio3h4i34og'


'''
    --------与任务本有关的路由--------

    /todo             访问“任务列表页面”，实现查询任务功能
    /todo_add              访问“新建任务页面”
    /add_check        处理新建任务表单，实现添加任务功能
    /finish           将任务状态修改为“已完成”
    /unfinish         将任务状态修改为“未完成”
    /todo_delete      将任务状态修改为“删除”

'''


# 路由：返回“任务列表页面”
@app.route('/todo')
def todo():
    # 访问控制：如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')
    else:
        # 获取提交的科目（subject）
        subject = request.args.get('subject')
        if subject == None or subject == '全部':
            condition = {'username': username}
        else:
            condition = {'username': username, 'subject': subject}
        # 使用todo_find()函数查询符合条件的任务数据
        todos = todo_find(condition)
        options = ['全部', '语文', '数学', '英语', '编程']

        # 返回任务页面
        return render_template('todo.html',
                               t_username=username,
                               t_todos=todos,
                               t_options=options,
                               t_subject=subject)

# 路由：返回“添加任务页面”
@app.route('/todo_add')
def todo_add():
    # 访问控制：如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')
    # 已登录
    else:
        # 可选科目
        options = ['语文', '数学', '英语', '编程']
        # 当前日期
        date = get_today()
        return render_template('todo_add.html',
                           t_options=options,
                           t_date=date,
                           t_username=username)


# 路由：获取添加任务表单提交的数据，实现添加任务功能
@app.route('/add_check', methods=['POST'])
def add_check():
    # 组装一条任务数据todo
    todo = {
        'subject': request.form.get('subject'),
        'content': request.form.get('content'),
        '_id': str(uuid.uuid1()),
        'state': '未完成',
        'username': session.get('username'),
        'date': get_today()
    }

    # 将新任务增加到数据库中
    todo_insert(todo)

    # 重定向到任务本主页
    return redirect('/todo')


# 路由：实现将任务设置为“已完成”
@app.route('/finish')
def finish():
    # 访问控制：如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')

    else:
        # 获取超链接提交的数据（_id），赋值给变量_id
        _id = request.args.get('_id')
        # 使用todo_update()函数更改任务状态
        todo_update({'_id': _id}, 'state', '已完成')
        # 重定向到任务列表页面
        return redirect('/todo')


# 路由：实现将任务设置为“未完成”
@app.route('/unfinish')
def unfinish():
    # 如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')
    else:
        # 获取超链接提交的数据（_id），赋值给变量_id
        _id = request.args.get('_id')
        # 使用todo_update()函数更改任务状态
        todo_update({'_id': _id}, 'state', '未完成')
        # 重定向到任务列表页面
        return redirect('/todo')


# 路由：实现删除任务，即将任务状态改为“已删除”
@app.route('/todo_delete')
def todo_delete():
    # 如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')
    else:
        # 【提示】：获取超链接提交的数据（_id），赋值给变量_id
        _id = request.args.get(id)
        # 【提示】：使用todo_update()函数将任务状态改为“”"已删除"
        #           参数1：查询条件（根据_id查询）
        #           参数2：修改的键名（state）
        #           参数3：键名对应的新值（已删除）
        todo_update(_id,{'state':'已删除'})
        # 重定向到任务列表页面
        return redirect('/todo')


'''
    --------与任务本有关的自定义函数--------

    todo_insert()      存储新的任务
    todo_find()        根据条件查询任务
    get_today()         获取今天的日期(字符串)
    todo_update()     修改任务状态”

'''


# 函数：增加新的任务
def todo_insert(data):
    client = pymongo.MongoClient()
    db_todo = client['ybc']
    c_todo = db_todo['todo']
    c_todo.insert_one(data)


# 函数：根据条件查询任务
def todo_find(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_todo = db_ybc['todo']
    todos = c_todo.find(data)
    todo_list = []
    for i in todos:
        todo_list.append(i)
    return todo_list


# 函数：获取今天的日期(字符串)
def get_today():
    # 获取今天的日期
    today = time.strftime('%Y-%m-%d', time.localtime())
    # 返回今天的日期
    return today


# 函数：更改任务状态
def todo_update(condition, key, value):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_todo = db_ybc['todo']
    # 先根据_id查询到任务，再更新任务状态“state”
    todo = c_todo.find_one(condition)
    if todo != None:
        todo[key] = value
        c_todo.update(condition, todo)


'''
    --------与个人名片有关的路由--------

    '/add_info'：返回“填写个人名片表单”页面
    '/info'：返回“个人名片展示”页面

'''


# # 路由：返回“个人信息表单”页面
@app.route('/add_info')
def add_info():
    return render_template('add_info.html')


# 路由：返回“个人名片展示”页面
@app.route('/info', methods=['POST'])
def get_info():
    name = request.form['name']
    age = request.form['age']
    info = request.form['info']
    # 【提示5】获取数据名称"gender"的值，并保存在变量gender中
    gender = request.form['gender']
    # 【提示6】为模板变量t_gender赋值
    return render_template('info.html', t_name=name, t_age=age, t_info=info, t_gender=gender)


'''
    --------与日记有关的路由--------

    '/diary'：返回“写日记表单”页面
    '/detail'：返回“我的日记”页面

'''
# # 路由：返回“写日记表单”页面
@app.route('/diary')
def form():
    return render_template('diary.html')

# 路由：返回“我的日记”页面
@app.route('/detail', methods=['POST'])
def info():
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    weather = request.form['weather']
    title = request.form['title']
    diary = request.form['diary']
    return render_template('detail.html', t_year=year, t_month=month, t_day=day, t_weather=weather, t_title=title, t_diary=diary)

'''
    --------与星座有关的路由--------

    '/date'：返回输入日期的页面
    '/star'：返回星座页面
    
'''
# 路由：返回“生日表单页面”
@app.route('/date')
def birthday():
    return render_template('date.html')

# 路由：返回“星座详情页面”
@app.route('/star', methods=['POST'])
def star():
    month = int(request.form['month'])
    day = int(request.form['day'])
    dates = [20, 19, 21, 21, 21, 22, 23, 23, 23, 24, 23, 22]
    stars = ['摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座']
    if day < dates[month-1]:
        return render_template('star.html', t_star_data=star_data.star_data[month-1])
    else:
        # 摩羯座是第1位
        return render_template('star.html', t_star_data=star_data.star_data[0 if month == 12 else month])

'''
    --------与音乐达人有关的路由--------

    '/music'：返回页面

'''
# 骑上我心爱的小摩托
@app.route('/music')
def music():
    return render_template('骑上我心爱的小摩托.html')

'''
    --------与同学录有关的路由--------

    '/'：根据查询条件返回主页面，默认返回所有数据
    '/add'：返回添加/更改数据的页面
    '/insert'：新增或更改数据，并返回主页面
    '/delete'：删除数据并返回主页面

'''


@app.route('/contact',methods=['GET','POST'])
def contact():
    condition = {}
    name = request.form.get('name')
    if name:
        condition['name'] = name
    contact_list = find_data(condition)
    return render_template('contact.html',t_contact_list=contact_list)



@app.route('/add',methods=['GET','POST'])
def add():
    condition = {}
    contact_list = find_data(condition)
    id = request.args.get('_id')
    if id != None:
        session['_id'] = id
        data_list = find_data({'_id':id})[0]
        return render_template('add.html',t_data_list = data_list,t_contact_list=contact_list)
    else:
        data_list = {'name':'','gender':'','age':'','number':''}
        return render_template('add.html',t_data_list = data_list,t_contact_list=contact_list)



@app.route('/insert',methods=['GET','POST'])
def insert():
    contact = {}
    contact['name'] = request.form.get('name')
    contact['age'] = request.form.get('age')
    contact['gender'] = request.form.get('gender')
    contact['number'] = request.form.get('number')
    id = session.get('_id')
    if id != None:
        contact['_id'] = id
        update_data(id, contact)
        session.clear()
        return redirect('/contact')
    else:
        contact['_id'] = str(uuid.uuid1())
        insert_data(contact)
        return redirect('/contact')



@app.route('/delete',methods=['GET','POST'])
def delete():
    id = request.args.get('_id')
    delete_data(id)
    return redirect('/contact')




'''
    --------与注册有关的路由--------

    /register         访问注册页面
    /register_check    处理注册表单，实现注册功能

'''


# 路由：访问“注册页面”
@app.route('/register')
def register():
    return render_template('register.html')


# 路由：处理注册表单，将注册用户存入数据库
@app.route('/register_check', methods=['POST'])
def register_check():
    username = request.form['username']
    pwd = request.form['password']

    user_list = find_user({'username': username})
    if len(user_list) == 0:

        user = {'username': username, 'pwd': pwd}
        insert_user(user)

        # 注册成功，重定向到“登录页面”
        return redirect('/login')
    else:
        return render_template('register.html',
                               t_username=username,
                               t_msg='用户名已经存在')


'''
    --------与登录有关的路由--------

    /login           访问登录页面
    /login_check     处理登录表单，实现登录功能

'''


# 路由：访问“登陆页面”
@app.route('/login')
def login():
    return render_template('login.html')


# 路由：处理登录表单，实现登录功能
@app.route('/login_check', methods=['POST'])
def login_check():
    username = request.form['username']
    pwd = request.form['password']

    user_list = find_user({'username': username, 'pwd': pwd})

    if len(user_list) == 1:

        # 登录成功后，将用户名存入session。该数据的键：'username'
        session['username'] = username

        # 登录成功，重定向到“任务列表页面”
        return redirect('/main')
    else:
        return render_template('login.html', t_error='用户名或密码错误')


# 路由：用户退出登录
@app.route('/logout')
def logout():
    # 删除session中的登录用户名
    session.pop('username')
    # 退出登录后，重定向到登录页面
    return redirect('/login')

'''
    --------与翻译有关的路由--------

    /trans        返回翻译主页
    /do_trans     实现翻译功能

'''

# 路由：返回翻译主页
@app.route('/trans')
def index():

    username = session.get('username')
    if username == None:
        username = "游客"

    return render_template('trans.html', t_op='英译汉', t_username=username)


# 路由：实现翻译功能
@app.route('/do_trans')
def translate():
    username = session.get('username')
    if username == None:
        username = "游客"

    txt = request.args['txt']
    op = request.args['op']

    if op == '英译汉':
        result = ybc_trans.en2zh(txt)
    elif op == '汉译英':
        result = ybc_trans.zh2en(txt)

    return render_template('trans.html', t_txt=txt, t_result=result, t_op=op, t_username=username)

'''
    --------与欢迎界面有关的路由--------

    /welcome        返回欢迎页面
    /main           返回主页

'''
# 路由：返回欢迎页面
@app.route('/welcome')
def welcome():
    return render_template('welcome.html', t_my_name='壮猿')


# 路由：返回主页
@app.route('/main')
def main():
    # 获取登录的用户名
    username = session.get('username')

    # 如果获取结果为None，则表示未登录；否则，表示已登录
    if username != None:
        is_login = True
    else:
        is_login = False
        username = '游客'

    # 返回主页，将用户名和登录状态传给主页
    return render_template('main.html', t_username=username, t_is_login=is_login)

'''
    --------与英雄有关的路由--------

    /add_hero        返回英雄信息页面
    /hero_result     返回结果页面

'''
# 路由：返回“页面'form.html'
@app.route('/add_hero')
def add_hero():
    wits = [1, 2, 3, 4 , 5]
    return render_template('add_hero.html', t_wits=wits)


# 路由：返回“页问卷调查提交结果
@app.route('/hero_result', methods=['POST'])
def hero_result():
    name = request.form['name']
    defense = int(request.form['defense'])
    attack = int(request.form['attack'])
    love = int(request.form['love'])
    dress = int(request.form['dress'])
    wit = int(request.form['wit'])
    data = [defense, attack, love, dress, wit]
    return render_template('hero_result.html', t_data=data, t_name=name)


'''
    --------与书籍的路由--------

    /book        返回书籍展示页面
    /add_book    返回添加书籍页面
    /add_book_check    实现添加书籍功能

'''

# 路由：返回“书籍信息页面
@app.route('/book')
def book():
    data = get_data()
    return render_template('book.html', t_data=data)


# 路由：返回添加书籍页面
@app.route('/add_book')
def add_book():
    return render_template('add_book.html')


# 路由：返实现添加书籍
@app.route('/add_book_check', methods=['POST'])
def add_book_check():
    name = request.form['name']
    # info = request.form['info']
    img = get_path()
    book_data = {
        'name': name,
        'img': img
    }
    book_insert(book_data)
    return redirect('/book')


'''
    --------与书籍有关的自定义函数--------

    book_insert()：增加图片的函数
    book_find()： 查询图片的函数
    get_data()：获取默认书籍的函数
    get_path()：获取图片路径的函数

'''
# 定义函数：增加书籍
def book_insert(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_book = db_ybc['books']
    c_book.insert_one(data)


# 定义函数：查询书籍
def book_find(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_book = db_ybc['books']
    book_list = []
    books = c_book.find(data)
    for i in books:
        book_list.append(i)
    return book_list


def get_data():
    data = [
        {'name': '世界未解之谜', 'img': 'static/images/pic1.jpg'},
        {'name': '米小圈上学记', 'img': 'static/images/pic2.jpg'},
        {'name': '哈利波特', 'img': 'static/images/pic3.jpg'},
        {'name': '长袜子皮皮', 'img': 'static/images/pic4.jpg'},
        # {'name': '稻草人', 'img': 'static/images/pic5.jpg'}
    ]
    res = book_find({})
    for i in res:
        data.append(i)
    return data


# 获取图片路径
def get_path():
    image = request.files.get('img')
    path = ''

    if not image:
        filename = 'default.jpg'
        path = 'static/images/upload/' + filename
    else:
        filename = image.filename
        path = 'static/images/upload/' + filename
        image.save(path)
    return path


'''
    --------与同学录有关的自定义函数--------

    insert_data()：增加数据的函数
    delete_data()：删除数据的函数
    update_data()：更改数据的函数
    find_data()：查询数据的函数

'''
def insert_data(dict):
    client = pymongo.MongoClient()
    db_contact = client['db_contact']
    c_contact = db_contact['c_contact']
    c_contact.insert_one(dict)

def delete_data(id):
    client = pymongo.MongoClient()
    db_contact = client['db_contact']
    c_contact = db_contact['c_contact']
    condition = {'_id':id}
    res = find_data(condition)
    for i in res:
        c_contact.delete_one(i)

def update_data(id,contact):
    client = pymongo.MongoClient()
    db_contact = client['db_contact']
    c_contact = db_contact['c_contact']
    condition = {'_id':id}
    res = c_contact.find(condition)
    print(res)
    for i in res:
        c_contact.update(condition,contact)

def find_data(condition):
    client = pymongo.MongoClient()
    db_contact = client['db_contact']
    c_contact = db_contact['c_contact']
    res = c_contact.find(condition)
    contact_list = []
    for i in res:
        contact_list.append(i)
    return contact_list


'''
    --------与登录、注册有关的自定义函数--------

    insert_user()     将注册用户数据存入数据库
    find_user()       根据条件查找注册用户信息
'''


# 函数:将注册用户数据存入数据库
def insert_user(user):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_ybc = client['ybc']
    c_user = db_ybc['user']
    c_user.insert_one(user)


# 函数：根据指定条件查找注册用户信息
def find_user(condition):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_ybc = client['ybc']
    c_user = db_ybc['user']
    res = c_user.find(condition)
    user_list = []
    for item in res:
        user_list.append(item)
    return user_list


if __name__ == '__main__':
    app.run(port=5001,debug=True)


from flask import Flask, render_template, request, redirect, session
import pymongo
import uuid
import time

app = Flask(__name__)
# 设置密钥
app.secret_key = '833/dik902#d'


'''
    --------与任务本有关的路由--------

    /todo             访问“任务列表页面”，实现查询任务功能

'''
# 路由：返回“任务列表页面”
@app.route('/todo')
def todo():
    # 没有登录，不能访问
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


# 路由：返回"新建任务页面"
# 【提示1】设置资源路径为："/add"
@app.route('/add')
def add():
    # 没有登录，不能访问
    username = session.get('username')
    if username == None:
        return redirect('/login')
    # 已登录
    else:
        # 可选科目
        options = ['语文', '数学', '英语', '编程']
        # 【提示2】使用get_today()方法获取当前日期，并保存在变量date中
        get_today()
        # 【t_to提示1】使用render_template方法返回"add.html"
        # 【提示2】模板变量赋值（科目模板变量:t_options，日期模板变量:t_date）
        return '00000'



# 路由：实现新建任务功能
@app.route('/add_check', methods=['POST'])
def add_check():
    # 【提示3】组装一条任务数据todo：
    #        'subject': 由表单提交(post方式)
    #        'content': 由表单提交(post方式)
    #        '_id': 使用uuid功能模块获取
    #        'state': 默认未完成
    #        'username': 从session中获取
    #        'date': 使用get_today函数获取
    todo = {
        'subject': '00000',
        'content': '00000',
        '_id': '00000',
        'state': '00000',
        'username': '00000',
        'date': '00000'
    }

    # 【提示4】使用todo_insert函数将新任务增加到数据库中
    00000

    # 【提示4】重定向到任务本主页
    return '00000'


'''
    --------与任务本有关的自定义函数--------
    todo_find()        根据条件查询任务

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


# ----------下面的代码实现用户注册、登录、退出（勿动）--------------

'''
    --------与注册有关的路由--------

    /register         访问注册页面
    /register_check    处理注册表单，实现注册功能

'''


# 路由：返回注册页面”
@app.route('/register')
def register():
    return render_template('register.html')


# 路由：实现注册功能
@app.route('/register_check', methods=['POST'])
def register_check():
    username = request.form['username']
    pwd = request.form['pwd']
    # 查询账号是否注册
    result = user_find({'username': username})
    if result == []:
        user_data = {'username': username, 'pwd': pwd}
        user_insert(user_data)

        # 注册成功，重定向到“登录页面”
        return redirect('/login')
    else:
        return render_template('register.html',
                               t_username=username,
                               t_error='此账号已注册')


'''
    --------与登录有关的路由--------

    /login           访问登录页面
    /login_check     处理登录表单，实现登录功能

'''


# 路由：返回登录页面”
@app.route('/login')
def login():
    return render_template('login.html')


# 路由：实现登录功能
@app.route('/login_check', methods=['POST'])
def login_check():
    username = request.form['username']
    pwd = request.form['pwd']

    result = user_find({'username': username, 'pwd': pwd})

    if result == []:

        return render_template('login.html', t_error='账号或密码错误')

    else:
        # 登录成功后，将账号（username）存入session
        session['username'] = username

        # 重定向到“任务列表页面”
        return redirect('/todo')


# 路由：用户退出登录
@app.route('/logout')
def logout():
    # 删除session中的登录用户名
    session.pop('username')
    # 退出登录后，重定向到登录页面
    return redirect('/login')


'''
    --------与登录、注册有关的自定义函数--------

    user_insert()     将注册用户数据存入数据库
    user_find()       根据条件查找注册用户信息
'''

# 函数:将注册用户数据存入数据库
def user_insert(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_user = db_ybc['user']
    c_user.insert_one(data)


# 函数：根据指定条件查找注册用户信息
def user_find(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_user = db_ybc['user']
    users = c_user.find(data)
    user_list = []
    for i in users:
        user_list.append(i)
    return user_list


if __name__ == '__main__':
    app.run(port=5001, debug=True)
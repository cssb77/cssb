from flask import Flask, render_template, request, redirect, session
import pymongo
import time
import uuid

app = Flask(__name__)
# 设置密钥
app.secret_key = '833/dik902#d'

'''
    --------与任务本有关的路由--------

    /todo             访问“任务列表页面”，实现查询任务功能
    /add              访问“新建任务页面”
    /add_check        处理新建任务表单，实现添加任务功能
    /finish           将任务状态修改为“已完成”
    /unfinish         将任务状态修改为“未完成”
    /delete           将任务状态修改为“删除”

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
        # ☆☆☆【提示1】修改html文件路径为："todo/todo.html"
        return render_template('todo.html',
                               t_username=username,
                               t_todos=todos,
                               t_options=options,
                               t_subject=subject)


# 路由：返回“新建任务页面”
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
        # 当前日期
        date = get_today()
        # ☆☆☆【提示1】修改html文件路径为："todo/add.html"
        return render_template('add.html',
                               t_options=options,
                               t_date=date)


# 路由：实现新建任务功能
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
    # 如果没有登录，则重定向到登录页面
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


# 路由：实现将任务设置为“删除”
@app.route('/delete')
def delete():
    # 如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')
    else:
        # 获取超链接提交的数据（_id），赋值给变量_id
        _id = request.args.get('_id')
        # 使用todo_update()函数更改任务状态
        todo_update({'_id': _id}, 'state', '已删除')

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


# ----------下面的代码实现用户注册、登录、退出（勿动）--------------

'''
    --------与注册有关的路由--------

    /register         访问注册页面
    /register_check    处理注册表单，实现注册功能

'''


# 路由：返回注册页面
@app.route('/register')
def register():
    # ☆☆☆【提示1】修改html文件路径为："user/register.html"
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
        # ☆☆☆【提示1】修改html文件路径为："user/register.html"
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
    # ☆☆☆【提示1】修改html文件路径为："user/login.html"
    return render_template('login.html')


# 路由：实现登录功能
@app.route('/login_check', methods=['POST'])
def login_check():
    username = request.form['username']
    pwd = request.form['pwd']
    result = user_find({'username': username, 'pwd': pwd})
    if result == []:
        # ☆☆☆【提示1】修改html文件路径为："user/login.html"
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
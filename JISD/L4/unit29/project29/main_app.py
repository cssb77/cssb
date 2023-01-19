from flask import Flask, render_template, request, redirect, session
import pymongo

# 创建Flask对象app
app = Flask(__name__)
# 设置密钥
app.secret_key = '833/dik902#d'


'''
    --------与任务本有关的路由--------

    /todo             访问“任务列表页面”，实现查询任务功能

'''
# 路由：实现查询功能，返回“任务列表页面”
@app.route('/todo')
def todo():
    # 如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')
    else:
        # 【提示1】创建数据库查询条件
        condition = {'username',username}
        # 【提示1】使用todo_find()函数查询符合条件的任务数据
        tobos = todo_find(condition)
        # 【提示1】为模板变量t_username、t_todos赋值，显示账号和任务
        return render_template('todo.html',t_todos = tobos,t_username=username)



'''
    --------与任务本有关的自定义函数--------
    todo_find()        根据条件查询任务
    
'''

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





# ----------下面的代码实现用户注册、登录、退出（勿动）

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
    result = user_find({'username':username})
    if result == []:
        user_data = {'username':username, 'pwd':pwd}
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

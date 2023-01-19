from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)

# 增加用户
def user_insert(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_user = db_ybc['user']
    c_user.insert_one(data)

# 查询用户
def user_find(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_user = db_ybc['user']
    user_list = []
    users = c_user.find(data)
    for i in users:
        user_list.append(i)
    return user_list

# -------------------------- 注册 -----------------------------

# 路由：返回“注册表页面
@app.route('/register')
def register():
    return render_template('register.html')


# 路由：实现注册功能
@app.route('/register_check', methods=['POST'])
def register_check():
    username = request.form['username']
    pwd = request.form['pwd']
    result = user_find({'username': username})
    if result == []:
        user_data = {'username': username, 'pwd': pwd}
        user_insert(user_data)
        return render_template('result.html')
    else:
        return render_template('register.html', t_error='此账号已注册', t_username=username)


# -------------------------- 登录 -----------------------------

# 路由：返回“登录页面
# 【提示1】设置资源路径为：“”"/login"
@app.route('/login')
def login():
    # 【提示1】 通过render_template方法返回"login.html"
    return render_template('login.html')


# 路由：实现登录功能
@app.route('/login_check', methods=['POST'])
def login_check():
    username = request.form['username']
    pwd = request.form['pwd']
    # 【提示2】 使用user_find函数查询账号密码是否正确，将查询结果保存在变量result中
    result = user_find({'username':username,'pwd':pwd})
    # 【提示2】 判断result是否为空列表: 如果result为空列表，返回"登录失败"
    if result==[]:
        return render_template('login.html',t_error="登录失败")
    #否则，返回"登录成功"
    # 【提示3】如果result为空列表，返回login.html，模板变量t_error赋值为"账号或密码错误"
    # 【提示4】如果result不为空列表，返回ok.html
    else:
        return render_template('ok.html',t_error="登录成功")


if __name__ == '__main__':
    app.run(port=5001, debug=True)



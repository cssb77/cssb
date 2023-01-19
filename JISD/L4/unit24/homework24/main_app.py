from flask import Flask, render_template, request, redirect
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
        # 【提示1】重定向到"/login"
        return render_template('/login')
    else:
        return render_template('register.html', t_error='此账号已注册')


# -------------------------- 登录 -----------------------------

# 路由：返回“登录页面
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
        # 【提示2】重定向到"/main"
        return render_template('/main')


# 路由：返回主页面
@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(port=5001, debug=True)



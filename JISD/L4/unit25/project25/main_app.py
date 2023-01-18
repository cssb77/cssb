from flask import Flask, render_template, request, redirect,session
import pymongo

app = Flask(__name__)
app.secret_key = 'secret-key'

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
        return redirect('/login')
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
        # 【提示3】 向字典session中存储username键值对，值为username变量
        session['username']=username
        return redirect('/main')

# 路由：返回主页面
@app.route('/main')
def main():
    # 【提示4】 从字典session中取出数据，存储在变量username中
    username=session['username']

    # 【提示5】 使用get方法从字典session中取出数据，存储在变量username中


    # 【提示4】 为模板变量t_username赋值，值为username变量
    return render_template('main.html',t_usernane=username)

if __name__ == '__main__':
    app.run(port=5001, debug=True)



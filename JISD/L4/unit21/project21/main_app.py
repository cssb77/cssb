from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)

# 增加用户
def user_insert(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_user = db_ybc['user']
    # 【提示3】将data插入c_user集合中
    00000

# 查询用户
def user_find():
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_user = db_ybc['user']
    user_list = []
    users = c_user.find()
    for i in users:
        user_list.append(i)
    return user_list


# 路由：返回“密码练习”页面
@app.route('/pwd')
def password():
    return render_template('password.html')


# 路由：实现密码提交功能，返回“所提交的密码
@app.route('/pwd_level', methods=['POST'])
def pwd_submit():
    pwd = request.form['pwd']
    return render_template('strength.html', t_pwd=pwd)


# 路由：返回“注册表单”页面
@app.route('/register')
def register():
    return render_template('register.html')


# 路由：实现注册功能，返回“注册结果”页面
@app.route('/register_check', methods=['POST'])
def register_check():
    username = request.form['username']
    pwd = request.form['pwd']
    # 【提示3】将账号和密码组装成字典格式的数据，并保存在变量user_data中
    # 字典格式：{'键1': 值1, '键2': 值2}
    00000
    # 【提示3】使用函数user_insert，并把user_data作为参数传入
    00000
    return render_template('result.html', t_pwd=pwd)


if __name__ == '__main__':
    app.run(port=5001, debug=True)



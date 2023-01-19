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


# 路由：返回“注册表单”页面
@app.route('/register')
def register():
    return render_template('register.html')


# 路由：实现注册功能，返回“注册结果”页面
@app.route('/register_check', methods=['POST'])
def register_check():
    username = request.form['username']
    pwd = request.form['pwd']
    result = user_find({'username': username})
    # 【提示1】判断列表result是否为空:
    #         如果为空列表，返回："无同名";
    #         否则，返回"有同名";
    # 【提示2】将账号和密码组装成一条字典数据，增加到数据库中，返回页面result.html
    # 【提示3】如果result不是空列表，返回注册页面
    # 【提示4】为register.html中的模板变量赋值，t_error="此账号已注册"
    # 【提示5】为register.html中的模板变量赋值，t_username=username
    


if __name__ == '__main__':
    app.run(port=5001, debug=True)



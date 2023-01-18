from flask import Flask, render_template, request, redirect,session
import pymongo
import ybc_trans


# 创建Flask对象app
app = Flask(__name__)

# secret_key加密
app.secret_key = 'zy666888'

# -------------------------- 翻译 -----------------------------

# 路由：返回“翻译表单”页面
# 路由：返回“翻译表单”⻚⾯
@app.route('/trans')
def trans():
 # 【提示1】从session字典中获取键名为'username'的 值
 username = session.get('username')
 # 【提示2】判断登录状态，如果登录可以访问翻译⻚⾯，否则显示登录⻚⾯
 # 【提示2】对username进⾏判断，如果值为None则重定向到'/login'路由，否则显示翻译⻚⾯
 if username == None:
     return redirect('/login')
 else:
     return render_template('trans.html',t_lang='英译汉', t_username=username)

# 路由：实现翻译功能，返回“翻译结果”页面
@app.route('/do_trans')
def do_trans():
    username = session.get('username')
    text = request.args['text']
    lang = request.args['lang']
    if lang == '英译汉':
        result = ybc_trans.en2zh(text)
    else:
        result = ybc_trans.zh2en(text)
    return render_template('trans.html', t_username=username, t_text=text, t_result=result, t_lang=lang)

# -------------------------- 管理数据函数 -----------------------------

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

# -------------------------- 注册、登录 -----------------------------

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
        session['username'] = username
        return redirect('/trans')

# 路由：实现退出
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')

if __name__ == '__main__':
    app.run(port=5001,debug=True)
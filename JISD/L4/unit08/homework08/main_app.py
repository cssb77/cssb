from flask import Flask, render_template

app = Flask(__name__)

# 路由：返回'欢迎页面'
# 【提示3】修改模板变量t_name的值（可以为自己的名字）
@app.route('/')
def C():
    return render_template('welcome.html', t_name='姬宇翔')

# 路由：返回'我的主页'
# 【提示3】修改模板变量t_name的值（可以为自己的名字）
@app.route('/main')
def main():
    return render_template('main.html', t_name='姬宇翔')

@app.route("/welcome")
def welcome():
    return render_template('welcome.html', t_name='姬宇翔')
@app.route("/b")
def b():
    return render_template('1.html')

if __name__ == '__main__':
    app.run(port=5001,debug=True)

from flask import Flask, render_template

app = Flask(__name__)

# 路由：返回'index1'
@app.route('/index1')
def index1():
    return render_template('index1.html')

# 路由：返回'欢迎页面'
@app.route('/welcome')
def welcome():
    return render_template('welcome.html', t_name='XXX')

# 路由：返回'我的主页'
@app.route('/main')
def main():
    return render_template('main.html', t_name='XXX')

if __name__ == '__main__':
    app.run(port=5001,debug=True)

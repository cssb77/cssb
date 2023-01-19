from flask import Flask

app = Flask(__name__)


# 定义路由，资源路径为''
@app.route('/nae')
# 补充功能函数的返回值，返回自己的姓名
def name():
    return jiyuxiang


# 定义路由，资源路径为''
@app.route('/age')
# 补充功能函数的返回值，返回自己的年龄
def age():
    return 11

if __name__ == '__main__':
    app.run(port = 5001, debug = True)
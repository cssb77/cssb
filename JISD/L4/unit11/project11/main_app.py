# 【提示3】导入request对象
from flask import Flask, render_template

app = Flask(__name__)


# 路由：返回“表单页面”
@app.route('/index')
def index():
    return render_template('index.html')


# 路由：返回“壮猿图片页面”
# 【提示2】设置服务器接收get请求
@app.route('/hello'method=["GET"])
def hello():
    # 【提示3】获取数据名称nickname的值，并保存在变量nickname中
    00000
    # 【提示3】为模板变量t_nickname赋值
    return render_template('info.html')


if __name__ == '__main__':
    app.run(port=5001, debug=True)



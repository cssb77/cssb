from flask import Flask, render_template, request

app = Flask(__name__)


# 路由：返回“多行文本输入框”页面
@app.route('/index')
def index():
    return render_template('index.html')


# 路由：返回"个人简介"
@app.route('/text', methods=['POST'])
def text():
    # 【提示2】获取数据名称"info"的值，保存在变量info中，并返回info
    00000
    # 【提示2】返回info
    return '00000'


# 路由：返回“个人信息表单”页面
@app.route('/form')
def form():
    return render_template('form.html')


# 路由：返回“个人名片展示”页面
@app.route('/info', methods=['POST'])
def card():
    name = request.form['name']
    age = request.form['age']
    # 【提示4】获取数据名称"info"的值，保存在变量info中
    00000
    # 【提示4】打印info
    00000
    # 【提示5】分别为模板变量t_name, t_age, t_info赋值，格式为：变量1=值1,变量2=值2,变量3=值3
    return render_template('info.html')


if __name__ == '__main__':
    app.run(port=5001, debug=True)



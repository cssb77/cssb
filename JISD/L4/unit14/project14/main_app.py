from flask import Flask, render_template, request, redirect

app = Flask(__name__)


# 路由：返回“选择天气”页面
@app.route('/index')
def index():
    return render_template('index.html')


# 路由：返回“展示最喜欢的天气”页面
@app.route('/best', methods=['GET'])
def best():
    # 若天气weather存在，展示天气页面
    if 'weather' in request.args:
        weather = request.args['weather']
        return render_template('weather.html', t_weather=weather)
    # 天气不存在返回当前页面
    else:
        return redirect('/index')


# # 路由：返回“个人信息表单”页面
@app.route('/form')
def form():
    return render_template('form.html')


# 路由：返回“个人名片展示”页面
@app.route('/info', methods=['POST'])
def get_info():
    name = request.form['name']
    age = request.form['age']
    info = request.form['info']
    # 【提示5】获取数据名称"gender"的值，并保存在变量gender中
    gender = request.form["gender"]
    # 【提示6】为模板变量t_gender赋值
    return render_template('info.html', t_name=name, t_age=age, t_info=info, t_gender=gender)


if __name__ == '__main__':
    app.run(port=5001, debug=True)



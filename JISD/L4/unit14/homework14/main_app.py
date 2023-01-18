from flask import Flask, render_template, request

app = Flask(__name__)


# # 路由：返回“写日记表单”页面
@app.route('/diary')
def form():
    return render_template('diary.html')


# 路由：返回“我的日记”页面
@app.route('/detail', methods=['POST'])
def info():
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    weather = request.form['weather']
    title = request.form['title']
    diary = request.form['diary']
    return render_template('detail.html', t_year=year, t_month=month, t_day=day, t_weather=weather, t_title=title, t_diary=diary)


if __name__ == '__main__':
    app.run(port=5001, debug=True)



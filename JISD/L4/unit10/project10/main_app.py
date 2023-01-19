from flask import Flask, render_template

app = Flask(__name__)


# 路由：返回“表单页面”
@app.route('/index')
def trans():
    return render_template('index.html')


# 路由：返回“壮猿图片页面”
# 【提示2】：补充定义路由语句中的资源路径，资源路径为: '/submit'
@app.route('/00000')
def submit():
    return render_template('photo.html')


if __name__ == '__main__':
    app.run(port=5001, debug=True)



# 从flask模块导入Flask
from flask import Flask,render_template
app = Flask(__name__)

# 【提示1】 定义路由，资源路径为'/1'
@app.route('/2')
def eeee():
    return render_template('1.tml')
# 【提示1】 定义函数index1()，使用render_template方法，返回模板'1.html'

# 【提示2】 返回模板'2.html'



if __name__ == '__main__':
    app.run(port=5001,debug=True)



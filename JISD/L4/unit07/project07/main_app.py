from flask import Flask, render_template
import time

app = Flask(__name__)

# 路由：返回"index1.html"
# 【任务1】：使用render_template方法返回"index1.html"页面，并为模板变量t_name赋值
# 【任务3】：为模板变量t_class赋值
@app.route('/index1')
def index1():
    00000

# 路由：返回"我的主页"
# 【任务4】：为模板变量t_name、t_time赋值
@app.route('/main')
def main():
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('main.html', 00000, 00000)

if __name__ == '__main__':
    app.run(port=5001,debug=True)

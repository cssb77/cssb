from flask import Flask,render_template

app = Flask(__name__)

# 骑上我心爱的小摩托
#【提示2】实现返回已添加样式的模板文件
@app.route('/music')
def music():
    # 在render_template方法中修改模板文件
   return render_template('少年.html')



if __name__ == '__main__':
    app.run(port=5001,debug=True)

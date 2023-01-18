from flask import Flask,render_template

app = Flask(__name__)

# 少年
@app.route('/1')
def sn():
    return render_template('少年.html')

# 稻香
@app.route('/2')
def dx():
    return render_template('稻香.html')

# 卡路里
@app.route('/3')
def kl():
    return render_template('卡路里.html')

# 青春修炼手册
@app.route('/4')
def qc():
    return render_template('青春修炼手册.html')

# 夜空中最亮的星
@app.route('/5')
def yk():
    return render_template('夜空中最亮的星.html')

# 骑上我心爱的小摩托
@app.route('/6')
def mt():
    return render_template('骑上我心爱的小摩托.html')

if __name__ == '__main__':
    app.run(port=5001,debug=True)
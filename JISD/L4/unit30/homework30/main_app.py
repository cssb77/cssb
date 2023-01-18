from flask import Flask, render_template, request

app = Flask(__name__)


# 路由：返回“页面'form.html'
@app.route('/form')
def form():
    wits = [1, 2, 3, 4 , 5]
    return render_template('form.html', t_wits=wits)


# 路由：返回“页问卷调查提交结果
@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    defense = int(request.form['defense'])
    attack = int(request.form['attack'])
    love = int(request.form['love'])
    dress = int(request.form['dress'])
    wit = int(request.form['wit'])
    data = [defense, attack, love, dress, wit]
    return render_template('result.html', t_data=data, t_name=name)



if __name__ == '__main__':
    app.run(port=5001, debug=True)



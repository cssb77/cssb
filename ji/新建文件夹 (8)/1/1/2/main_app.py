from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)
# 【提示3】修改模板变量t_name的值（可以为自己的名字）
def user_find(data):
    client = pymongo.MongoClient()
    db_ybc = client['ji']
    c_user = db_ybc['ji2']
    user_list = []
    users = c_user.find(data)
    for i in users:
        user_list.append(i)
    return user_list
@app.route('/')
def C():
    return render_template('welcome.html', t_name='姬宇翔')
@app.route('/main')
def main():
    return render_template('main.html', t_name='姬宇翔')
@app.route("/welcome")
def welcome():
    return render_template('welcome.html', t_name='姬宇翔')
@app.route("/b")
def b():
    return render_template('1.html')
@app.route("/w")
def w():
    return render_template('2.html')
@app.route("/r")
def r():
    return render_template('4.html')
@app.route('/date')
def birthday():
    return render_template('date.html')
@app.route('/star',methods=["POST"])
def star():
    month = int(request.form['month'])
    day = int(request.form['day'])
    dates = [20, 19, 21, 21, 21, 22, 23, 23, 23, 24, 23, 22]
    stars = ['摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座']
    if day < dates[month-1]:
        return render_template('star.html', t_star_data=star_data.star_data[month-1])
    else:
        # 摩羯座是第1位
        return render_template('star.html', t_star_data=star_data.star_data[0 if month == 12 else month])
@app.route('/ji1')
def ji1():
    return render_template('ji1.html')
@app.route('/ji2',methods=['POST'])
def ji2():
    ji1 = request.form['jiq']
    print('/n'+ji1)
    f = open('1.txt','r')
    e = f.readlines()
    client = pymongo.MongoClient()
    ab_ji = client['ji']
    c_ji = ab_ji['ji1']
    c_ji.insert_one({'1':ji1})
    result = user_find({'1':ji1})
    print(str(result))
    rr = ''
    if e =='':
        f = open('1.txt','w')
        f.write(':  ')
        f.close()
        rr = ''
    if ji1 != '':
        if result == []:
            f = open('1.txt', 'a')
            f.write('{'+ji1+"}")
            f.close()
        elif result != []:
            f = open('1.txt', 'r')
            rr = f.readlines()
            rr = str(rr)
            f.close()
    if ji1=='0558222':
        f = open('2.txt', 'r')
        rr = str(f.readlines())
        f.close()
    elif ji1=='utyuu':
        client = pymongo.MongoClient()
        db_ji = client['ji']
        c_ji2 = db_ji['ji2']
        user_list = []
        users = c_ji2.find()
        for i in users:
            user_list.append(i)
        rr = user_list

    return render_template('ji2.html',t_ji2=ji1,t_jiq=rr)
@app.route('/ji3')
def ji3():
    return render_template('ji4.html')
@app.route('/ji4',methods=['POST'])
def ji4():
    jie = request.form['jie']
    rrr = {'1':jie}
    client = pymongo.MongoClient()
    db_ji = client['ji']
    c_ji1 = db_ji['ji2']
    c_ji1.insert_one(rrr)
    return render_template('ji3.html')

if __name__ == '__main__':
    app.run(port=5001,debug=True)

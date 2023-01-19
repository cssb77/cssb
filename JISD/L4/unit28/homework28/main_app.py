from flask import Flask,render_template,redirect,request,session
import pymongo
import uuid

app = Flask(__name__)
app.secret_key = 'zy666888'

# 所有路由
# '/phonebook'：，返回主页面，默认返回所有数据
# '/add'：返回添加数据的页面
# '/find'：，根据查询条件返回主页面
# '/insert'：新增或更改数据，并返回主页面

@app.route('/phonebook')
def phonebook():
    res = phonebook_find({})
    return render_template('phonebook.html',t_res=res)


@app.route('/add')
def add():
    res = phonebook_find({})
    return render_template('add.html',t_res=res)


@app.route('/insert',methods=['GET','POST'])
def insert():
    phonebook = {}
    phonebook['name'] = request.form.get('name')
    phonebook['age'] = request.form.get('age')
    phonebook['gender'] = request.form.get('gender')
    phonebook['number'] = request.form.get('number')
    phonebook['_id'] = str(uuid.uuid1())
    phonebook_insert(phonebook)
    return redirect('/phonebook')


@app.route('/find',methods=['POST'])
def find():
    name = request.form.get('name')
    res = phonebook_find({'name': name})
    return render_template('phonebook.html', t_res=res)


# 需要使用的函数
# phonebook_insert()：增加数据的函数
# phonebook_find()：查询数据的函数

def phonebook_insert(data):
    client = pymongo.MongoClient()
    db_class = client['class']
    c_phonebook = db_class['phonebook']
    c_phonebook.insert_one(data)


def phonebook_find(data):
    client = pymongo.MongoClient()
    db_class = client['class']
    c_phonebook = db_class['phonebook']
    res = c_phonebook.find(data)
    phonebook_list = []
    for i in res:
        phonebook_list.append(i)
    return phonebook_list


if __name__ == '__main__':
    app.run(port=5001,debug=True)
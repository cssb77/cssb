from flask import Flask,render_template,redirect,request,session
import pymongo

app = Flask(__name__)
app.secret_key = 'zy666888'


# 定义函数：增加书籍
def book_insert(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_book = db_ybc['books']
    c_book.insert_one(data)


# 定义函数：查询书籍
def book_find(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_book = db_ybc['books']
    book_list = []
    books = c_book.find(data)
    for i in books:
        book_list.append(i)
    return book_list


def get_data():
    data = [
        {'name': '世界未解之谜', 'img': 'static/images/pic1.jpg'},
        {'name': '米小圈上学记', 'img': 'static/images/pic2.jpg'},
        {'name': '哈利波特', 'img': 'static/images/pic3.jpg'},
        {'name': '长袜子皮皮', 'img': 'static/images/pic4.jpg'},
        # {'name': '稻草人', 'img': 'static/images/pic5.jpg'}
    ]
    res = book_find({})
    for i in res:
        data.append(i)
    return data


# 获取图片路径
def get_path():
    image = request.files.get('img')
    path = ''

    if not image:
        filename = 'default.jpg'
        path = 'static/images/upload/' + filename
    else:
        filename = image.filename
        path = 'static/images/upload/' + filename
        image.save(path)
    return path


# 路由：返回“书籍信息页面
@app.route('/book')
def book():
    data = get_data()
    return render_template('book.html', t_data=data)


# 路由：返回添加书籍页面
@app.route('/add')
def add():
    return render_template('add.html')


# 路由：返实现添加书籍
@app.route('/add_check', methods=['POST'])
def add_check():
    name = request.form['name']
    # info = request.form['info']
    img = get_path()
    book_data = {
        'name': name,
        'img': img
    }
    book_insert(book_data)
    return redirect('/book')

if __name__ == '__main__':
    app.run(port=5001,debug=True)
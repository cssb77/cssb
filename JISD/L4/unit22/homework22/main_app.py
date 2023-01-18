from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)

# 定义函数：增加宠物
def pet_insert(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_pet = db_ybc['pet']
    c_pet.insert_one(data)

# 定义函数：查询宠物
def pet_find(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_pet = db_ybc['pet']
    pet_list = []
    pets = c_pet.find(data)
    for i in pets:
        pet_list.append(i)
    return pet_list


# 路由：返回“宠物信息填写”页面
@app.route('/pet')
def pet():
    return render_template('pet.html')


# 路由：实现添加宠物功能
@app.route('/info', methods=['POST'])
def info():
    path = get_path()
    name = request.form['name']
    age = request.form['age']
    info = request.form['info']
    # 【提示】将名字、年龄、介绍、图片路径path组装成一条字典数据，保存在变量pet_data中
    pet_datd = {'name':name,'age':age,'info':info}
    # 【提示】使用pet_insert函数将pet_data增加到数据库中
    pet_insert(pet_datd)
    return render_template('info.html', t_name=name, t_age=age, t_info=info, t_path=path)


# 获取图片路径
def get_path():
    image = request.files.get('image')
    path = ''

    if not image:
        filename = 'default.jpeg'
        path = 'static/images/' + filename
    else:
        filename = image.filename
        path = 'static/images/' + filename
        image.save(path)
    return path


if __name__ == '__main__':
    app.run(port=5001, debug=True)



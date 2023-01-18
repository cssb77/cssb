import pymongo
import uuid


# 创建景点数据(字典)
scene1 = {'_id': str(uuid.uuid1()), 'name': '桂林山水', 'city': '桂林'}
scene2 = {'_id': str(uuid.uuid1()), 'name': '故宫', 'city': '北京'}
scene3 = {'_id': str(uuid.uuid1()), 'name': '冰雪大世界', 'city': '哈尔滨'}
scene4 = {'_id': str(uuid.uuid1()), 'name': '玉龙雪山', 'city': '丽江'}
scene5 = {'_id': str(uuid.uuid1()), 'name': '龙门石窟', 'city': '洛阳'}
scene6 = {'_id': str(uuid.uuid1()), 'name': '日月潭', 'city': '台中'}
scene7 = {'_id': str(uuid.uuid1()), 'name': '大雁塔', 'city': '西安'}
scene8 = {'_id': str(uuid.uuid1()), 'name': '布达拉宫', 'city': '拉萨'}


# 函数：增加景点
def scene_insert(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_scene = db_ybc['scene']
    c_scene.insert_one(data)


# 练习：使用函数scene_insert()，将景点数据添加到集合c_scene中
scene_insert(scene1)
scene_insert(scene2)
scene_insert(scene3)
scene_insert(scene4)
scene_insert(scene5)
scene_insert(scene6)
scene_insert(scene7)
scene_insert(scene8)


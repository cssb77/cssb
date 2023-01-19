import pymongo
import uuid

# 创建函数：修改景点名称
def scene_update(condition, key, value):
    # 连接数据库
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_scene = db_ybc['scene']
    # 查询符合条件的数据
    scene = c_scene.find_one(condition)
    if scene != None:
        # 修改原数据
        scene[key] = value
        # 更新数据库中对应的数据
        c_scene.update(condition, scene)

#----------------------------修改数据--------------------------

# 【提示2】使用函数：修改景点名称（查询条件为"name"，将name改为"兵马俑"）










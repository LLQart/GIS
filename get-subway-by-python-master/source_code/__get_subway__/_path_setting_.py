# -*- coding: utf-8 -*-
"""
@time: Created on Wed Feb 17 22:51:12 2021

@use: 用于文件路径的预制，在执行正式的文件之前需要对文件夹位置进行预设值

@author: zoro
"""

import os               #用于创建并未存在的文件夹
'''
整个文件存储的嵌套关系为：
|<D:/Python/get_subway_from_AMap>: 根目录

|-</jsondata>: 原始json数据目录

|-</final_data>: 转化数据文件目录

|--</shp_data>: shapefile文件目录
|---</gaode>高德坐标系文件目录
|---</wgs84>WGS坐标系文件目录
|---</baidu>百度坐标系文件目录

|--</geojson_data>: geojson文件目录
|---</gaode>高德坐标系文件目录
|---</wgs84>WGS坐标系文件目录
|---</baidu>百度坐标系文件目录
'''

# |<D:/Python/get_subway_from_AMap>: 根目录
root = 'D:/vscode/pythonscript/GISlianxi/exract_subwaylines/get-subway-by-python-master/source_code/'

##-----------------------以下数据谨慎变更，已经预设路径名称-----------------------##
# |-</jsondata>: 原始json数据目录
json_data = root + 'jsondata/'  # 原始json数据目录

# |-</final_data>: 转化数据文件目录
final_data = root + 'final_data/'  # 最终数据目录

# |--</shp_data>: shapefile文件目录
shp_data = final_data + 'shp_data/'
# |---</gaode>高德坐标系文件目录
shp_data_gaode_line = shp_data + 'line/gaode/'
shp_data_gaode_point = shp_data + 'point/gaode/'
# |---</wgs84>WGS坐标系文件目录
shp_data_wgs84_line = shp_data + 'line/wgs84/'
shp_data_wgs84_point = shp_data + 'point/wgs84/'
# |---</baidu>百度坐标系文件目录
shp_data_baidu_line = shp_data + 'line/baidu/'
shp_data_baidu_point = shp_data + 'point/baidu/'

# |--</geojson_data>: geojson文件目录
geojson_data = final_data + 'geojson_data/'
# |---</gaode>高德坐标系文件目录
geojson_data_gaode_line = geojson_data + 'line/gaode/'
geojson_data_gaode_point = geojson_data + 'point/gaode/'
# |---</wgs84>WGS坐标系文件目录
geojson_data_wgs84_line = geojson_data + 'line/wgs84/'
geojson_data_wgs84_point = geojson_data + 'point/wgs84/'
# |---</baidu>百度坐标系文件目录
geojson_data_baidu_line = geojson_data + 'line/baidu/'
geojson_data_baidu_point = geojson_data + 'point/baidu/'

total_path = [root,json_data,final_data,
              shp_data_gaode_line, shp_data_gaode_point,
              shp_data_wgs84_line, shp_data_wgs84_point,
              shp_data_baidu_line, shp_data_baidu_point,
              geojson_data_gaode_line, geojson_data_gaode_point,
              geojson_data_wgs84_line, geojson_data_wgs84_point,
              geojson_data_baidu_line, geojson_data_baidu_point
              ]

def pre_path():
    try:
        for path_i in range(len(total_path)):
            if not os.path.exists(total_path[path_i]):
                os.makedirs(total_path[path_i])
    except:
        print("Problems in model <pre_path>")

def path(file_type,geo_type,coor_type):
    try:
        if file_type == 'shp':
            if geo_type == 'point':
                if coor_type == 'gaode':
                    path = shp_data_gaode_point
                elif coor_type == 'wgs84':
                    path = shp_data_wgs84_point
                elif coor_type == 'baidu':
                    path = shp_data_baidu_point
                else:
                    print("确认坐标点的坐标系名称")
            elif geo_type == 'line':
                if coor_type == 'gaode':
                    path = shp_data_gaode_line
                elif coor_type == 'wgs84':
                    path = shp_data_wgs84_line
                elif coor_type == 'baidu':
                    path = shp_data_baidu_line
                else:
                    print("确认地铁线路的坐标系名称")
        elif file_type == 'geojson':
            if geo_type == 'point':
                if coor_type == 'gaode':
                    path = geojson_data_gaode_point
                elif coor_type == 'wgs84':
                    path = geojson_data_wgs84_point
                elif coor_type == 'baidu':
                    path = geojson_data_baidu_point
                else:
                    print("确认坐标点的坐标系名称")
            elif geo_type == 'line':
                if coor_type == 'gaode':
                    path = geojson_data_gaode_line
                elif coor_type == 'wgs84':
                    path = geojson_data_wgs84_line
                elif coor_type == 'baidu':
                    path = geojson_data_baidu_line
                else:
                    print("确认地铁线路的坐标系名称")
        else:
            print("确认文件类型名称")
        return path

    except:
        print("Problems in model <path>")

def raw_data_path():
    return json_data

pre_path()
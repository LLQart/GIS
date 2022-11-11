# -*- coding: utf-8 -*-
"""
@time: Created on Wed Feb 17 22:51:12 2021
@use : <_01_GetSubwayGeoInfo.py>用于清洗原始的json数据，获得高德坐标系的shp文件和geojson文件
@author: zoro
"""

import os
from __get_subway__ import _path_setting_ as ps         #用于预设文件路径
from __get_subway__ import _file_names_ as fn           #导入文件夹名称和文件名称获取模块
from __get_subway__ import get_subway_data as gd        #导入编写的数据清洗模块
from __get_subway__ import writer                       #导入geojson和shapefile文件读写模块
from geojson import FeatureCollection                   #完成geojson文件的编辑工作


def get_subway_geo():
    try:
        #获取所有城市目录
        city_menu = fn.file_name_reader(ps.raw_data_path())
        #在每个城市下进行数据汇总
        for city_i in range(len(city_menu)):
            try:
                #获取城市所有线路目录
                line_path = ps.raw_data_path() +city_menu[city_i]
                line_menu = fn.file_name_reader(line_path)

                #存储shp线文件的临时容器,换城市自动清空
                tem_subwayline_cor = []
                tem_subwayline_record = []
                #存储shp点文件的临时容器,换城市自动清空
                tem_subwaypoint_cor = []
                tem_subwaypoint_record = []

                #存储geojson文件的临时容器,换城市自动清空
                tem_line_features=[]
                tem_line_features_collect = []
                tem_point_features=[]
                tem_point_features_collect= []

                #如果城市文件夹下面没有数据则不再执行程序
                if len(line_menu)>0:
                    # 每条线路单独清洗数据
                    for line_i in range(len(line_menu)):
                        try:
                            '''
                            获取原始json数据地址：
                            json数据根目录+城市名称+线路文件保存名称
                            实际地址组成如下，注意添加中间的分割和文件后缀：
                            json_root + city_menu[city_i] + line_menu[line_i]
                            '''
                            # 获取线路json数据地址
                            city_json_path = ps.raw_data_path()  + city_menu[city_i] + '/' + line_menu[line_i]
                            # 读取原始json数据
                            raw_data = fn.file_reader(city_json_path)

                            # 清洗线路数据
                            ##清洗shp数据
                            gd.shp_line(raw_data, tem_subwayline_cor, tem_subwayline_record)
                            ##清洗geojson数据
                            gd.geojson_line(raw_data, tem_line_features)

                            # 清洗站点数据
                            ##清洗shp数据
                            gd.shp_point(raw_data, tem_subwaypoint_cor, tem_subwaypoint_record)
                            ##清洗geojson数据
                            gd.geojson_point(raw_data, tem_point_features)
                        except:
                            pass
                else:
                    pass

                #将所有线路的数据进行最终的保存
                ##保存线路数据
                ###保存shp文件
                shp_line_fold = ps.path('shp','line','gaode') + city_menu[city_i] + '/'
                if not os.path.exists(shp_line_fold):
                    os.makedirs(shp_line_fold)
                shp_line = shp_line_fold+ city_menu[city_i]+'.shp'
                writer.shp_line_writer(shp_line,tem_subwayline_cor,tem_subwayline_record)

                ###保存geojson文件
                geojson_line = ps.path('geojson','line','gaode')+city_menu[city_i]+'.geojson'
                tem_line_features_collect = FeatureCollection(tem_line_features)
                writer.geojson_writer(geojson_line,tem_line_features_collect)

                ##保存站点数据
                ###保存shp文件
                shp_point_fold = ps.path('shp','point','gaode') +city_menu[city_i]+'/'
                if not os.path.exists(shp_point_fold):
                    os.makedirs(shp_point_fold)
                shp_point = shp_point_fold + city_menu[city_i] + '.shp'
                writer.shp_point_writer(shp_point, tem_subwaypoint_cor, tem_subwaypoint_record)

                ###保存geojson文件
                geojson_point = ps.path('geojson','point','gaode') + city_menu[city_i] + '.geojson'
                tem_point_features_collect = FeatureCollection(tem_point_features)
                writer.geojson_writer(geojson_point, tem_point_features_collect)
            except:
                pass
    except:
        pass

if __name__ == '__main__':
    get_subway_geo()

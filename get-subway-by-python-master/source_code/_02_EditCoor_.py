# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:51:12 2021
@author: zoro
"""
import os                                               #用于文件的读写
import shapefile                                        #用于shapefile文件的处理
import json                                             #用于json文件的基本操作
import geopandas                                        #用于geojson数据的处理
from shapely import geometry                            #用于geopandas中矢量数据处理
from __get_subway__ import _path_setting_ as ps         #用于预设文件路径
from __get_subway__ import _file_names_ as fn           #导入文件夹名称和文件名称获取模块
from __get_subway__ import coor_trans as ct             #用于坐标点的坐标转换
from __get_subway__ import writer                       #导入geojson和shapefile文件读写模块

'''
整体思路为
循环读取各个城市已经形成的高德坐标系shp文件 ----> 
分别转化为各个城市的shp文件 ----> 读取坐标点信息 ----> 
使用坐标转化模块批量转化 ----> 写入相应坐标系的文件夹
'''

def trans_shp_point(reproject):
    try:
        city_point_menu = fn.file_name_reader(ps.path('shp','point','gaode'))
        for city_i in range(len(city_point_menu)):
            try:
                # 空的shp坐标列表用于创建新的shp文件
                tem_cor_data_list = []
                # 空的shp属性信息列表用于创建新的shp文件
                tem_record_data_list = []
                tem_city_path = ps.path('shp','point','gaode') + city_point_menu[city_i] + '/' + city_point_menu[city_i] + '.shp'
                sf = shapefile.Reader(tem_city_path, encoding='utf-8')
                shapes = sf.shapes()
                records = sf.records()
                if len(shapes) > 0:
                    for shape_i in range(len(shapes)):
                        if reproject == 'wgs84':
                            shp_cor = ct.gcj02_to_wgs84(shapes[shape_i].points[0][0],
                                                        shapes[shape_i].points[0][1])
                        elif reproject == 'baidu':
                            shp_cor = ct.gcj02_to_bd09(shapes[shape_i].points[0][0],
                                                       shapes[shape_i].points[0][1])
                        else:
                            print("请检查坐标系名称")
                        tem_cor_data_list.append(shp_cor)
                        tem_record_data_list.append(records[shape_i])

                    if reproject == 'wgs84':
                        tem_point_path = ps.path('shp', 'point', 'wgs84')+ city_point_menu[city_i] + '/' + city_point_menu[city_i] + '.shp'
                        #print("导出shp——wgs84", tem_point_path)
                    elif reproject == 'baidu':
                        #print("导出shp——baidu")
                        tem_point_path = ps.path('shp', 'point', 'baidu')+ city_point_menu[city_i] + '/' + city_point_menu[city_i] + '.shp'
                    else:
                        print("确认坐标系名称")

                    writer.shp_point_writer(tem_point_path, tem_cor_data_list, tem_record_data_list)
                else:
                    pass

            except:
                print(city_point_menu[city_i],"point problem")
    except:
        print("Problems in model <trans_shp_point>")

def trans_shp_line(reproject):
    try:
        city_line_menu = fn.file_name_reader(ps.path('shp', 'line', 'gaode'))
        for city_i in range(len(city_line_menu)):
            try:
                # 空的shp坐标列表用于创建新的shp文件
                tem_cor_data_list = []
                # 空的shp属性信息列表用于创建新的shp文件
                tem_record_data_list = []
                # 拼接读取文件路径
                tem_city_path = ps.path('shp', 'line', 'gaode') + city_line_menu[city_i] + '/' + city_line_menu[city_i] + '.shp'
                #print(tem_city_path)
                # 读取shp文件
                sf = shapefile.Reader(tem_city_path, encoding='cp936')
                #print(sf)
                # 获取形状文件
                shapes = sf.shapes()
                # 获取属性信息
                records = sf.records()
                
                if len(shapes) > 0:
                    for shape_i in range(len(shapes)):
                        '''
                        读取的线路点数据格式如下：
                        [(lon1,lat1),(lon2,lat2),(lon3,lat3),...]
                        因此需要对每条线路的列表进行内循环
                        '''
                        tem_line_cor_list = []
                        
                        for tem_i in range(len(shapes[shape_i].points)):
                            if reproject == 'wgs84':
                                tem_cor_data_list_line = ct.gcj02_to_wgs84(shapes[shape_i].points[tem_i][0],
                                                                           shapes[shape_i].points[tem_i][1])
                            elif reproject == 'baidu':
                                tem_cor_data_list_line = ct.gcj02_to_bd09(shapes[shape_i].points[tem_i][0],
                                                                          shapes[shape_i].points[tem_i][1])
                            else:
                                print("确认坐标系名称")

                            tem_line_cor_list.append(tem_cor_data_list_line)
                        '''
                        单条线路的地理空间数据,应该是列表嵌套格式,例如
                        [[[120.11,30.5],[122.11,32.5]]]
                        shp_cor应该是这样的样式
                        '''
                        tem_cor_data_list.append([tem_line_cor_list])

                        tem_record_data_list.append(records[shape_i])
                    if reproject == 'wgs84':
                        tem_line_path = ps.path('shp', 'line', 'wgs84')+ city_line_menu[city_i] + '/' + city_line_menu[city_i] + '.shp'
                        print("导出shp——wgs84", tem_line_path)
                    elif reproject == 'baidu':
                        tem_line_path = ps.path('shp', 'line', 'baidu')+ city_line_menu[city_i] + '/' + city_line_menu[city_i] + '.shp'
                        print("导出shp——baidu", tem_line_path)
                    else:
                        print("确认坐标系名称")
                    writer.shp_line_writer(tem_line_path, tem_cor_data_list, tem_record_data_list)
                else:
                    pass
            except:
                print("导出错误啦！！")
    except:
        print("Problems in model <trans_shp_line>")

def trans_geojson_point(reproject):
    try:
        city_point_menu = fn.file_name_reader(ps.path('geojson','point','gaode'))
        for city_i in range(len(city_point_menu)):
            try:
                path = ps.path('geojson','point','gaode') + city_point_menu[city_i]
                temp_data = geopandas.read_file(path)
                temp_data_geometry = temp_data.geometry
                #创建用于存放GeoSeries中坐标点的空列表
                geometry_list = []
                record_list=[]
                #依次把各个站点的坐标点进行转换
                #属性信息直接继承之前数据的
                for point_i in range(len(temp_data_geometry)):
                    if reproject == 'wgs84':
                        point_cor = ct.gcj02_to_wgs84(temp_data_geometry[point_i].x,
                                                               temp_data_geometry[point_i].y)
                        geometry_list.append(geometry.Point(point_cor[0],point_cor[1]))
                    elif reproject == 'baidu':
                        point_cor = ct.gcj02_to_bd09(temp_data_geometry[point_i].x,
                                                      temp_data_geometry[point_i].y)
                        geometry_list.append(geometry.Point(point_cor[0], point_cor[1]))
                    else:
                        print("确认坐标系名称")
                    #直接沿用原来数据的属性信息
                    station_num = temp_data.station_num	[point_i]
                    line_name = temp_data.line_name[point_i]
                    station_name= temp_data.station_name[point_i]
                    status = temp_data.status[point_i]

                    #集合形成属性列表
                    temp_list = (station_num,line_name,station_name,status)
                    record_list.append(temp_list)
                geojson_file = geopandas.GeoDataFrame(data=record_list,
                                                      geometry=geometry_list,
                                                      columns=['station_num','line_name',
                                                               'station_name','status'])
                if reproject == 'wgs84':
                    tem_point_path = ps.path('geojson', 'point', 'wgs84') + city_point_menu[city_i]
                elif reproject == 'baidu':
                    tem_point_path = ps.path('geojson', 'point', 'baidu') + city_point_menu[city_i]
                else:
                    print("确认坐标系名称")
                geojson_file.to_file(tem_point_path,driver='GeoJSON',encoding = 'utf8')

            except:
                pass
    except:
        print(city_point_menu[city_i],"Problems in model <trans_geojson_point>")

def trans_geojson_line(reproject):
    try:
        city_line_menu = fn.file_name_reader(ps.path('geojson','line','gaode'))
        for city_i in range(len(city_line_menu)):
            try:
                path = ps.path('geojson','line','gaode') + city_line_menu[city_i]
                temp_data = geopandas.read_file(path)
                temp_data_geometry = temp_data.geometry

                # 创建用于存放GeoSeries中坐标点的空列表
                geometry_list = []
                record_list = []

                # 依次把各条线路各个的坐标点进行转换
                # 属性信息直接继承之前数据的
                for line_i in range(len(temp_data_geometry)):
                    #用于临时存储线路关键点坐标的列表
                    line_list=[]
                    #此处获取了每条线路的各个关键点坐标数据，格式为[(lng1,lon1),(lng2,lon2),(lng3,lon3),...]
                    temp_cor_list = list(temp_data_geometry[line_i].coords)
                    #这里开始循环变换每个坐标点数据
                    for line_point_i in range(len(temp_cor_list)):
                        if reproject == 'wgs84':
                            line_point = ct.gcj02_to_wgs84(temp_cor_list[line_point_i][0],
                                                           temp_cor_list[line_point_i][1])
                            line_list.append(line_point)
                        elif reproject == 'baidu':
                            line_point = ct.gcj02_to_bd09(temp_cor_list[line_point_i][0],
                                                           temp_cor_list[line_point_i][1])
                            line_list.append(line_point)
                        else:
                            print("确认坐标系名称")
                    geometry_list.append(geometry.LineString(line_list))

                    #沿用属性信息
                    key_name = temp_data.key_name[line_i]
                    line_name = temp_data.line_name[line_i]
                    front_name = temp_data.front_name[line_i]
                    terminal_name = temp_data.terminal_name[line_i]
                    status = temp_data.status[line_i]

                    temp_list = (key_name,line_name,front_name,terminal_name,status)
                    record_list.append(temp_list)

                geojson_file =geopandas.GeoDataFrame(data=record_list,
                                                     geometry = geometry_list,
                                                     columns=['keyname', 'line_name',
                                                              'front_name','terminal_name',
                                                              'status'])
                if reproject == 'wgs84':
                    tem_line_path = ps.path('geojson', 'line', 'wgs84') + city_line_menu[city_i]
                elif reproject == 'baidu':
                    tem_line_path = ps.path('geojson', 'line', 'baidu') + city_line_menu[city_i]
                else:
                    print("确认坐标系名称")
                geojson_file.to_file(tem_line_path, driver='GeoJSON', encoding='utf8')
            except:
                pass
    except:
        print("Problems in model <trans_geojson_line>")

def _trans_main_():
    try:
        '''
        目前可以选择转换的坐标系仅有两种：
        1.'wgs84'：无偏移的WGS84坐标系
        2.'baidu'：百度坐标系
        '''
        trans_shp_point('wgs84')
        trans_shp_point('baidu')
        trans_shp_line('wgs84')
        trans_shp_line('baidu')
        trans_geojson_point('wgs84')
        trans_geojson_point('baidu')
        trans_geojson_line('wgs84')
        trans_geojson_line('baidu')
        print("succefful!!!")

    except:
        print("Problems in model <_trans_main_>")

if __name__ == '__main__':
    _trans_main_()
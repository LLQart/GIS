# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:51:12 2021

use: 用于写入geojson和shapefile文件。

@author: zoro
"""
import os
import shapefile                   #用于shapefile文件的编写
import json                        #用于json文件的处理
import osr                         #用于坐标系的定义和转换


def shp_point_writer(shp_path,cor_data_list,record_data_list):
        try:
            #这里定义shapefile文件读写的地址
            shape_file = shapefile.Writer(shp_path)
            '''
            创建站点的属性:
            1.station_num：站点数量编号
            2.linename：线路名称
            3.station_name：站点名称
            4.status：运营/在建状态
            '''
            shape_file.field("station_num", 'C', '50')
            shape_file.field("linename", 'C', '50')
            shape_file.field("station_name", 'C', '50')
            shape_file.field("status", 'C', '50')
            
            '''
            循环写入站点的地理空间数据,仅使用单个坐标点,例如(120.11,30.5)
            循环写入站点属性数据
            '''
            for i in range(len(cor_data_list)):
                #shape_file.point()函数用于写入经纬度坐标
                shape_file.point(cor_data_list[i][0], cor_data_list[i][1])
                #shape_file.record()函数用于写入属性信息
                shape_file.record(record_data_list[i][0].encode('cp936'), record_data_list[i][1].encode('cp936'),
                                  record_data_list[i][2].encode('cp936'), record_data_list[i][3].encode('cp936'))
            #shape_file.close用于常规的文件读写结束后声明停止
            shape_file.close

            # 定义投影
            proj = osr.SpatialReference()
            # 这里将坐标系定义为WGS84
            proj.SetWellKnownGeogCS('WGS84')
            wkt = proj.ExportToWkt()
            # 点坐标写入投影
            f_point = open(shp_path.replace(".shp", ".prj"), 'w')
            f_point.write(wkt)
            f_point.close()
        except:
            print("shp_point_writer")

def shp_line_writer(shp_path,cor_data_list,record_data_list):
        try:
            shape_file = shapefile.Writer(shp_path)
            '''
            创建站点的属性:
            1.key_name：关键字名称
            2.linename：线路名称
            3.front_name：起始站名称
            4.terminal_name：终点站名称
            5.status：运营/在建状态
            '''
            shape_file.field("key_name", 'C', '50')
            shape_file.field("linename", 'C', '50')
            shape_file.field("front_name", 'C', '50')
            shape_file.field("terminal_name", 'C', '50')
            shape_file.field("status", 'C', '50')
            '''
            循环写入线路的地理空间数据,应该是列表嵌套格式,例如[[120.11,30.5],[122.11,32.5]]
            循环写入线路属性数据                       
            '''
            for i in range(len(cor_data_list)):
                shape_file.line(cor_data_list[i])
                #print(record_data_list[i][0])
                shape_file.record(record_data_list[i][0].encode('cp936'), record_data_list[i][1].encode('cp936'),
                                  record_data_list[i][2].encode('cp936'), record_data_list[i][3].encode('cp936'),
                                  record_data_list[i][4].encode('cp936'))
            shape_file.close

            # 定义投影
            proj = osr.SpatialReference()
            # 这里将坐标系定义为WGS84
            proj.SetWellKnownGeogCS('WGS84')
            wkt = proj.ExportToWkt()

            # 线坐标写入投影
            f_line = open(shp_path.replace(".shp", ".prj"), 'w')
            f_line.write(wkt)
            f_line.close()
        except:
            print("shp_line_writer")


def geojson_writer(file_path, geojson_data):
    try:
        with open(file_path,'w') as f:
            json.dump(geojson_data,f)
    except:
        print("geojson数据保存失败")
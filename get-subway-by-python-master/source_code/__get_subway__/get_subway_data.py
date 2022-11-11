# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:51:12 2021

use: 用于原始数据清洗的模块

@author: zoro
"""

from geojson import Feature,Point, LineString

def shp_line(busline_list,cor_list,record_list):
    try:
        '''
        由于busline_list当中包含了双向的地铁线路以及不同分段的地铁数据，因此需要
        1.剔除重复线路的数据，
        2.选用busline_list列表中奇数序号的元素
        3.剔除type不为2的元素,只有type为2才是地铁线路数据
        4.判断status是1还是3，1就是在运营，3就是在建    
        '''

        for line_id in range(0, len(busline_list), 2):
            try:
                if (busline_list[line_id]['type'] == '2'):
                    linename = busline_list[line_id]['name'].split("(")[0]
                    front_name = busline_list[line_id]['front_name']
                    terminal_name = busline_list[line_id]['terminal_name']
                    # 这里需要组合经纬度坐标
                    lons = busline_list[line_id]['xs'].split(",")
                    lats = busline_list[line_id]['ys'].split(",")
                    cor = []
                    for cor_i in range(len(lons)):
                        tem_cor = [float(lons[cor_i]), float(lats[cor_i])]
                        cor.append(tem_cor)
                    # 这里的cor的内容已经是[[cor1],[cor2]]格式
                    cor_list.append([cor])
                    
                    # 这里赋予线路属性信息
                    ## 这里说整体线路编号，例如地铁1号线，不涉及第几期
                    key_name = busline_list[line_id]['key_name']
                    ## 这里判断地铁线路运营状态
                    if (busline_list[line_id]['status'] == '1'):
                        status = '运营中'
                    else:
                        status = '建设中'
                    ## 归纳属性信息
                    tem_record_list = [key_name, linename, front_name,
                                           terminal_name, status]
                    record_list.append(tem_record_list)
                else:
                        continue
            except:
                print("shp_line线路循环出错")
                break
    except:
        print("")

def shp_point(busline_list,cor_list,record_list):
    try:
        '''
        由于busline_list当中包含了双向的地铁线路以及不同分段的地铁数据，因此需要
        1.剔除重复线路的数据，
        2.选用busline_list列表中奇数序号的元素
        3.剔除type不为2的元素  
        4.判断status是1还是3，1就是在运营，3就是在建  
        '''
        for stations_id in range(0, len(busline_list), 2):
            try:
                # 判断buslist下的type属性是否为2，即是否为地铁数据
                if (busline_list[stations_id]['type'] == '2'):
                    line_name = busline_list[stations_id]['name'].split('(')[0]
                    # 这里循环提取站点坐标
                    for station_id in range(len(busline_list[stations_id]['stations'])):
                        try:
                            station_name = busline_list[stations_id]['stations'][station_id]['name']
                            station_num = busline_list[stations_id]['stations'][station_id]['station_num']
                            station_cor_raw = busline_list[stations_id]['stations'][station_id]['xy_coords'].split(
                                    ";")
                            station_lon = float(station_cor_raw[0])
                            station_lat = float(station_cor_raw[1])
                            station_cor = (station_lon, station_lat)
                            
                            # 这里将点坐标追加到点空间信息列表
                            cor_list.append(station_cor)
                            
                            # 这里将点坐标属性信息追加到属性列表
                            ## 这里判断地铁线路运营状态
                            if (busline_list[stations_id]['status'] == '1'):
                                status = '运营中'
                            else:
                                status = '建设中'
                            tem_record_list = [station_num, line_name, station_name, status]
                            record_list.append(tem_record_list)
                        except:
                            print("站点提取出错")
                else:
                    continue
            except:
                print("shp_point站点循环出错")
                break
    except:
            print("")

def geojson_line(busline_list,line_features):
    '''
    由于busline_list当中包含了双向的地铁线路以及不同分段的地铁数据，因此需要
    1.剔除重复线路的数据，
    2.选用busline_list列表中奇数序号的元素
    3.剔除type不为2的元素
    4.判断status是1还是3，1就是在运营，3就是在建
    '''
    try:
        for line_id in range(0, len(busline_list), 2):
            try:
                if (busline_list[line_id]['type'] == '2'):
                    linename = busline_list[line_id]['name'].split("(")[0]
                    # 这里说整体线路编号，例如地铁1号线，不涉及第几期
                    key_line_name = busline_list[line_id]['key_name']
                    front_name = busline_list[line_id]['front_name']
                    terminal_name = busline_list[line_id]['terminal_name']
                    # 这里需要组合经纬度坐标
                    lons = busline_list[line_id]['xs'].split(",")
                    lats = busline_list[line_id]['ys'].split(",")
                    cor = []
                    for cor_i in range(len(lons)):
                        tem_cor = (float(lons[cor_i]), float(lats[cor_i]))
                        cor.append(tem_cor)
                        ## 这里判断地铁线路运营状态
                    if (busline_list[line_id]['status'] == '1'):
                        status = "运营中"
                    else:
                        status = "建设中"
                    line_feature = Feature(geometry=LineString(tuple(cor)), properties={
                            "key_name":key_line_name,
                            "line_name": linename,
                            "front_name": front_name,
                            "terminal_name": terminal_name,
                            "status":status})
                    line_features.append(line_feature)
                else:
                    continue
            except:
                print("geojson_line线路循环出错")
                break
    except:
        print("geojson_line线路获取错误")

def geojson_point(busline_list,subwaypointFeatures):
        '''
        由于busline_list当中包含了双向的地铁线路以及不同分段的地铁数据，因此需要
        1.剔除重复线路的数据，
        2.选用busline_list列表中奇数序号的元素
        3.剔除type不为2的元素
        4.判断status是1还是3，1就是在运营，3就是在建
        '''
        try:

            for stations_id in range(0, len(busline_list), 2):
                try:
                    # 判断buslist下的type属性是否为2，即是否为地铁数据
                    if (busline_list[stations_id]['type'] == '2'):
                        line_name = busline_list[stations_id]['name']

                        # 这里循环提取站点坐标
                        for station_id in range(len(busline_list[stations_id]['stations'])):
                            try:
                                station_name = busline_list[stations_id]['stations'][station_id]['name']
                                station_num = busline_list[stations_id]['stations'][station_id]['station_num']
                                station_cor_raw = busline_list[stations_id]['stations'][station_id]['xy_coords'].split(
                                    ";")
                                station_lon = float(station_cor_raw[0])
                                station_lat = float(station_cor_raw[1])
                                station_cor = (station_lon, station_lat)
                                ## 这里判断地铁线路运营状态
                                if (busline_list[stations_id]['status'] == '1'):
                                    status = '运营中'
                                else:
                                    status = '建设中'
                                station_feature = Feature(geometry=Point(tuple(station_cor)), properties={
                                    "station_num": station_num,
                                    "line_name": line_name,
                                    "station_name": station_name,
                                    "status":status
                                })

                                subwaypointFeatures.append(station_feature)
                            except:
                                print("站点提取出错")
                    else:
                        continue
                except:
                    print("geojson_point站点循环出错")
                    break
        except:
            print("geojson_point站点获取错误")
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:51:12 20211

这一模块用于
1.文件夹下文件名称列表的获取
2.读取json文件并返回原始数据

@author: zoro
"""

import os
import json

def file_name_reader(file_name_path):
        try:
            file_name_list = os.listdir(file_name_path)
            return file_name_list
        except:
            print("")

def file_reader(file_path):
        try:
            with open(file_path,"r",encoding='utf-8') as rawjson_data:
                load_json = json.load(rawjson_data)
            busline_list = load_json['data']['busline_list']
            return busline_list
        except:
            print("")
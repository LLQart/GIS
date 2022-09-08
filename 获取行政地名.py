import xlrd
import os
import requests
import xlwt
from xlutils.copy import copy
from tqdm import tqdm



AK='22fcd3093365e8c7edaa86fb8b66e30b'

def Coord2Pos(lon,lat,town='true'):
    url = "https://restapi.amap.com/v3/geocode/regeo?output=json&location={0},{1}&key={2}&radius=1000&extensions=all".format(str(lon), str(lat),AK)
    res = requests.get(url)
    if res.status_code == 200:
        val = res.json()
        # print(val)
        val = val['regeocode']
        retVal = {'province': val['addressComponent']['province'], 'city': val['addressComponent']['city'],
                      'district': val['addressComponent']['district'], 'town': val['addressComponent']['township'],
                      'adcode': val['addressComponent']['adcode'],'town_code': val['addressComponent']['towncode'],
                      'street': val['addressComponent']['streetNumber']['street']}
        distance = float(3000)
        for i in range(len(val['pois'])):
            if val['pois'][i]['type'] =='地名地址信息;普通地名;村庄级地名':
                valdis = float(val['pois'][i]['distance'])
                if valdis < distance:
                    distance = valdis
                    retVal['village'] = val['pois'][i]['name']
        return retVal
    else:
        print('无法获取(%s,%s)的地理信息！' % (lat, lon))

def transform(lon, lat):
    url = "https://restapi.amap.com/v3/assistant/coordinate/convert?locations={0},{1}&coordsys=gps&key={2}".format(str(lon), str(lat),AK)
    res = requests.get(url)
    if res.status_code == 200:
        val = res.json()
        # print(val)
        if val['status'] == '1':
            # print("val")
            lon, lat = val['locations'].split(',')
            # print(val)
            # print(val[0]['x'], val[0]['y'])
            return lon, lat

# file_path = os.path.dirname(os.path.abspath(__file__))
# base_path = os.path.join(file_path, 'data.xlsx')
# book = xlrd.open_workbook('D:\Desktop\临县隐患点.xls', 'w+')
# sheet1 = book.sheets()[0]
# nrows = sheet1.nrows  #表格总行数
# ncols = sheet1.ncols #表格总列数
# row3_values = sheet1.row_values(2) 第3行值
# col3_values = sheet1.col_values(2) 第3列值
# cell_3_3 = sheet1.cell(2, 2).value 第3行第3列的单元格的值

book = xlrd.open_workbook(r'D:\workspace\晋西\离石区insar在册kml\矢量数据\隐患点.xls', 'w+')
sheet1 = book.sheets()[0]
nrows = sheet1.nrows  #表格总行数
ncols = sheet1.ncols #表格总列数

pbar = tqdm(range(nrows))#进度条
# 提取行政位置信息
val = []
town = []
for i,j in zip(range(1, nrows), pbar):
    lon, lat = transform(sheet1.cell(i, 3).value, sheet1.cell(i, 4).value)
    value = Coord2Pos(lon, lat)
    try:
        village = value['village']
    except:
        village = value['street']
    val.append(village)
    # print(value["town"])
    town.append(value["town"])
    # print("提取成功，提取进度{0}/{1}".format(i,nrows-1))
    err = '提取进度'
    pbar.set_description("Reconstruction loss: %s" %(err))

print('提取成功！！！')

# 写入表格
newWb = copy(book)#复制
newWs = newWb.get_sheet(0);#取sheet表
for i,j in zip(range(1, nrows), pbar):
    newWs.write(i, 5, town[i-1]);#写入 2行4列写入pass
    newWs.write(i, 6, val[i-1]);#写入 2行4列写入pass
    # print("写入数据，写入进度{0}/{1}".format(i, nrows-1))
    err = '写入进度'
    pbar.set_description("Reconstruction loss: %s" %(err))
print('写入成功！！！')

newWb.save('D:\Desktop\离石区隐患点.xls'); #保存至result路径













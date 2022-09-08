from osgeo import ogr
import os


driver = ogr.GetDriverByName('ESRI Shapefile')
#filename = 'C:/Users/gongwei/Documents/My eBooks/python_and_sage/GDAL python/test/ospy_data1/sites.shp'
filename = r"D:\vscode\pythonscript\image_deal\image-classified\随机森林分类\Python+Scikit-Learn+RandomForest\data\sample1.shp"
dataSource = driver.Open(filename,0)
if dataSource is None:
    print('could not open')
    os._exit(1)
print('done!')


# 读取数据层
layer = dataSource.GetLayer(0)
n = layer.GetFeatureCount()
print('feature count:', n)


# 读出上下左右边界
extent = layer.GetExtent()
print('extent:', extent)
print('ul:', extent[0], extent[3])
print('lr:', extent[1], extent[2])

# 读取某一要素feature
feat = layer.GetFeature(13)
fid = feat.GetField('类型')
print(fid)
feat = layer.GetFeature(0)
fid = feat.GetField('类型') #should be a different id
print (fid)

# 按顺序读取
# feat = layer.GetNextFeature()  #读取下一个
# while feat is not None:
#     print(feat.GetField('类型'), feat.GetField('id'))
#     feat = layer.GetNextFeature()
# feat.ResetReading()  #复位

# 提取feature的几何形状
geom = feat.GetGeometryRef()
geom.GetX()
geom.GetY()
print (geom)

# 释放内存
# feature.Destroy()
# 关闭数据源
# dataSource.Destroy()
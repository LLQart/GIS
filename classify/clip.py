from osgeo import gdal
import osgeo.ogr as ogr
# # tif输入路径，打开文件
# input_raster = r"C:/DEM/坡度.tif"
# # 栅格文件路径，打开栅格文件
# input_raster=gdal.Open(input_raster)
# #匹配文件名字，可以编写读取文件夹文件来替换
# name =['开县',..........., '石柱土家族自治县']
# for n in name:
#     #开始裁剪，一行代码
#     ds = gdal.Warp(n+".tif",#生成的栅格
#               input_raster,
#               format = 'GTiff',
#               #矢量文件
#               cutlineDSName = n+".shp",      
#               #cutlineWhere="FIELD = 'whatever'",
#               dstNodata = 0)


rasterPath=r"D:\vscode\pythonscript\image_deal\image-classified\随机森林分类\Python+Scikit-Learn+RandomForest\data\BOA Reflectance-10m_MTD_MSIL2A.tif"
shpPath=r"D:\vscode\pythonscript\image_deal\image-classified\随机森林分类\Python+Scikit-Learn+RandomForest\data\sample1.shp"
ds = gdal.Warp("test3.tif",#生成的栅格
               rasterPath,
               format = 'GTiff',
               #矢量文件
               cutlineDSName=shpPath,      
               #cutlineWhere="FIELD = 'whatever'",
               dstNodata = 0)
from tkinter.tix import Tree
from osgeo import gdal, ogr, osr
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class Point:
    def __init__(self,x,y):
        self.X =x  
        self.Y=y 

def getSubRaster(srcImage, polygonPoints):
    minX=10000000000000
    maxX=-minX
    minY=100000000000000000
    maxY=-minY

    for point in polygonPoints:
        if point.X<minX:minX=point.X
        if point.X>maxX:maxX=point.X
        if point.Y<minY:minY=point.Y
        if point.Y>maxY:maxY=point.Y
    leftX=minX
    upY=maxY
    rightX=maxX
    bottomY=minY
    transform = (srcImage.GetGeoTransform())
    lX = transform[0]#左上角点
    lY = transform[3]
    rX = transform[1]#分辨率
    rY = transform[5]

    wpos=int((leftX-lX)/rX)
    hpos=int((upY-lY)/rY)

    width=int((rightX-leftX)/rX)
    height=int((bottomY-upY)/rY)
    BandsCount = srcImage.RasterCount
    arr = srcImage.ReadAsArray(wpos,hpos,width,height)
    fixX=list()
    nodatavalue=srcImage.GetRasterBand(1).GetNoDataValue()
    #print(nodatavalue)
    #nodatavalue=0.
    for i in range(height):
        Y=upY+i*rY+.00001
        pointsindex=list()
        for k in range(len(polygonPoints)-1):
                point1=polygonPoints[k]
                point2=polygonPoints[k+1]
                if (point1.Y>=Y and point2.Y<=Y) or (point1.Y<=Y and point2.Y>=Y):
                    pointsindex.append(k)
        for j in range(width):
            count=0
            for m in (pointsindex):
                point1=polygonPoints[m]
                point2=polygonPoints[m+1]
                X=leftX+j*rX+.00001
                #print(point1, point2)
                if point1.X==point2.X:
                    intersectX=point1.X
                    if intersectX>X:count+=1
                else:
                    k=(point2.Y-point1.Y)/(point2.X-point1.X)
                    if k==0:
                        if X<point1.X or X<point2.X:
                            count+=1
                    else:
                        intersectX=(Y-point1.Y)/k+point1.X
                        if intersectX>X:count+=1

            if count%2==0:
                if BandsCount>1:
                    for bc in range(BandsCount):
                        arr[bc][i][j]=(nodatavalue)
                else:
                    arr[i][j]=-1
    #writeRaster("test2.tif",arr,srcImage,width,height,BandsCount,leftX,upY)
    #print(arr.shape)
    return arr,width,height,BandsCount,leftX,upY

def writeRaster(name,arr,inraster,width,height,bandscount,leftX=0,upY=0):
    #写入栅格数据
    transform = (inraster.GetGeoTransform())
    driver = gdal.GetDriverByName("GTiff")
    out = driver.Create(name,width,height,4,srcImage.GetRasterBand(1).DataType)

    out.SetGeoTransform([leftX,transform[1],transform[2],upY,transform[4],transform[5]])
    out.SetProjection(srcImage.GetProjectionRef())
    print(arr.shape)
    for i in range(arr.shape[0]):
        out.GetRasterBand(i+1).WriteArray(arr[i])
        # out.GetRasterBand(2).WriteArray(arr[1])
        # out.GetRasterBand(3).WriteArray(arr[2])
    out.FlushCache()
    out = None
    rds=None



def createDataSet(rasterPath, shpPath):
    srcImage = gdal.Open(rasterPath)
    transform = srcImage.GetGeoTransform()   # 获取换转6参数
    srcProj = srcImage.GetProjection()      # 获取投影信息
    spatial2=osr.SpatialReference()
    spatial2.ImportFromWkt(srcImage.GetProjectionRef())  # 使用栅格的投影信息

    shapef = ogr.Open(shpPath)
    lyr = shapef.GetLayer()
    spatial1=lyr.GetSpatialRef()   # 矢量投影信息
    #print('feature count:', lyr.GetFeatureCount())   # 获取元素数目
    ct=osr.CreateCoordinateTransformation(spatial1,spatial2)

    poly = lyr.GetNextFeature()

    trainX = list()       # 训练集样本
    trainY = list()       # 训练集标签
    while poly:
        #print(poly.GetField('类型'))
        geom = poly.GetGeometryRef() 
        #print(type(geom))
        pts = geom.GetGeometryRef(0)  # 获取集合对象
        #print(pts.GetPoints())
        value=poly.GetField('Id')
        #print(value)
        pointSet = []
        for pt in pts.GetPoints():
            #print(pt)
            PT = ct.TransformPoint(pt[0], pt[1], 0)
            #print(PT)
            pointSet.append(Point(PT[0], PT[1]))
        arr,width,height,BandsCount,leftX,upY = getSubRaster(srcImage, pointSet)
        for i in range(height):
                for k in range(width):
                    nodata=True
                    tem = list()
                    for bc in range(BandsCount):
                        v=int(arr[bc][i][k])
                        tem.append(v)
                        if v>0:nodata=False
                    if nodata:
                        continue
                    trainX.append(tem)
                    trainY.append(int(value))
        poly = lyr.GetNextFeature()
        #print(type(pts), pts.GetPointCount(),pts.GetPoints())   # 获取点位
        # points = []
        # for p in range(pts.GetPointCount()):
        #   points.append((pts.GetX(p), pts.GetY(p)))
        #print(points)
        #获取面积
        #print(pts.GetArea())
    print(np.array(trainX).shape, np.array(trainY).shape)
    print(trainX[0], trainY[0])
    print(trainX[5000], trainY[5000])
    return trainX, trainY


def trainModel(trainX,trainY):
    ct=None
    spatial1=None
    spatial2=None
    treenum = 100
    clf = RandomForestClassifier(n_estimators=treenum)
    clf.fit(trainX, trainY)#训练样本
    return clf

    


  

# if __name__=='__main__':
#     rasterPath=r"D:\vscode\pythonscript\image_deal\image-classified\随机森林分类\Python+Scikit-Learn+RandomForest\data\BOA Reflectance-10m_MTD_MSIL2A.tif"
#     shpPath=r"D:\vscode\pythonscript\image_deal\image-classified\随机森林分类\Python+Scikit-Learn+RandomForest\data\sample1.shp"
#     trainX, trainY = createDataSet(rasterPath, shpPath)
#     trainModel(trainX, trainY)
    
import operator
from re import A
from osgeo import gdal, gdal_array, osr
import shapefile
try:
    import Image, ImageDraw
except:
    from PIL import Image, ImageDraw

raster = "stretched.tif"
shp = "hancock/hancock"
output = "clip"

def imageToArray(i):
    a = gdal_array.numpy.fromstring(i.tobytes(), 'b')  
    a.shape = i.im.size[1], i.im.size[0]
    return a

def world2Pixel(geoMatrix, x, y):
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    pixel = int((x - ulX) / xDist)
    line = int((ulY - y) / yDist)
    return (pixel, line)

srcArray = gdal_array.LoadFile(raster)
srcImage = gdal.Open(raster)
geoTrans = srcImage.GetGeoTransform()
r = shapefile.Reader("{}.shp".format(shp))
#将图层扩展转为像素坐标
minX, minY, maxX, maxY = r.bbox
ulX, ulY = world2Pixel(geoTrans, minX, maxX)
lrX, lrY = world2Pixel(geoTrans, maxX, minY)
# 计算新图片的像素尺度
pxWidth = int(lrX - ulX)
pxHeight = int(lrY - ulY)
clip = srcArray[:,ulY:lrY, ulX:lrX]

geoTrans = list(geoTrans)
geoTrans[0] = minX
geoTrans[3] = maxY

pixels = []
for p in r.shape(0).points:
    pixels.append(world2Pixel(geoTrans,p[0],p[1]))
rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
print('hi',rasterPoly)
rasterize = ImageDraw.Draw(rasterPoly)
rasterize.polygon(pixels, 0)

mask = imageToArray(rasterPoly)
# print(mask)
clip = gdal_array.numpy.choose(mask, (clip, 0)).astype(gdal_array.numpy.uint8)

gdal_array.SaveArray(clip, "{}.tif".format(output), format="GTiff", prototype=raster)
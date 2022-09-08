from osgeo import gdal, gdalconst
import os

'''
GDAL数据驱动，与OGR数据驱动类似，需要先创建某一类型的数据驱动，再创建响应的栅格数据集。 
一次性注册所有的数据驱动，但是只能读不能写：gdal.AllRegister() 单独注册某一类型的数据驱动，这样的话可以读也可以写，可以新建数据集：
'''
filepath = r"D:\vscode\pythonscript\image_deal\image-classified\随机森林分类\Python+Scikit-Learn+RandomForest\data\BOA Reflectance-10m_MTD_MSIL2A.tif"

driver = gdal.GetDriverByName('HFA')
driver.Register()

# 打开已有的栅格数据集
fn = 'aster.img'
ds = gdal.Open(filepath, gdal.GA_ReadOnly)
if ds is None:
    print('Could not open ', fn)
    os._exit(1)

# 读取栅格数据集的x方向像素数，y方向像素数，和波段数
cols = ds.RasterXSize
rows = ds.RasterYSize
bands = ds.RasterCount
print(cols, rows, bands)

# GeoTransform是一个list，存储着栅格数据集的地理坐标信息  栅格数据集的坐标一般都是以左上角为基准的。
'''
adfGeoTransform[0] /* top left x 左上角x坐标*/
adfGeoTransform[1] /* w--e pixel resolution 东西方向上的像素分辨率*/
adfGeoTransform[2] /* rotation, 0 if image is "north up" 如果北边朝上，地图的旋转角度*/
adfGeoTransform[3] /* top left y 左上角y坐标*/
adfGeoTransform[4] /* rotation, 0 if image is "north up" 如果北边朝上，地图的旋转角度*/
adfGeoTransform[5] /* n-s pixel resolution 南北方向上的像素分辨率*/
'''
adfGeoTransform = ds.GetGeoTransform()


# 计算某一坐标对应像素的相对位置(pixel offset)，也就是该坐标与左上角的像素的相对位置，按像素数计算，计算公式如下：
'''
xOffset = int((x – originX) / pixelWidth)
yOffset = int((y – originY) / pixelHeight)
'''

#读取某一像素点的值，需要分两步 首先读取一个波段(band)：GetRasterBand(<index>)，其参数为波段的索引号 
# 然后用ReadAsArray(<xoff>, <yoff>, <xsize>, <ysize>)，读出从(xoff,yoff)开始，大小为(xsize,ysize)的矩阵。如果将矩阵大小设为1X1，
# 就是读取一个像素了。但是这一方法只能将读出的数据放到矩阵中，就算只读取一个像素也是一样。例如：
xOffset, yOffset = 0, 0
band = ds.GetRasterBand(1)
data = band.ReadAsArray(xOffset, yOffset, 1, 1)

#如果想一次读取一整张图，那么将offset都设定为0，size则设定为整个图幅的size，例如：
data = band.ReadAsArray(0, 0, cols, rows)
#data中读取某一像素的值，必须要用data[yoff, xoff]。注意不要搞反了。数学中的矩阵是[row,col]，而这里恰恰相反！这里面row对应y轴，col对应x轴。


'''
分块读取
如何更有效率的读取栅格数据？显然一个一个的读取效率非常低，将整个栅格数据集都塞进二维数组也不是个好办法，因为这样占的内存还是很多。
更好的方法是按块(block)来存取数据，只把要用的那一块放进内存。本周的样例代码中有一个utils模块，可以读取block大小。
'''
import utils
blockSize = utils.GetBlockSize(band)
xBlockSize = blockSize[0]
yBlockSize = blockSize[1]
# 平铺(tiled)，即栅格数据按block存储。有的格式，例如GeoTiff没有平铺，一行是一个block。Erdas imagine格式则按64x64像素平铺。 
# 如果一行是一个block，那么按行读取是比较节省资源的。 如果是平铺的数据结构，那么设定ReadAsArray()的参数值，让它一次只读入一个block，就是效率最高的方法了。
# 例如：
rows, cols, xBSize, yBSize = 13, 11, 5, 5
for i in range(0, rows, yBSize):
    if i + yBSize < rows:
        numRows = yBSize
    else:
        numRows = rows - i
        for j in range(0, cols, xBSize):
            if j + xBSize < cols:
                numCols = xBSize
            else:
                numCols = colsnumCols = cols - j
            data = band.ReadAsArray(j, i, numCols, numRows)


# band对象可以设定NoData值
#outBand.SetNoDataValue(-99)

# 还可以读取NoData值
#ND = outBand.GetNoDataValue()

#把缓存数据写入磁盘
#FlushCache()
import numpy as np
from osgeo import gdal
import pickle


# 定义图像打开方式
def image_open(image):
    data1 = gdal.Open(image)
    if data1 == "None":
        print("数据无法打开")
    return data1


# 定义模型打开方式
def model_open(model):
    data1 = open(model, "rb")
    data2 = pickle.load(data1)
    data1.close()
    return data2


# 定义图像保存
def writeTiff(im_data, im_geotrans, im_proj, path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape
    # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)
    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


# 定义相关参数
Image_FilePath = r"E:yynctryedata20180911_yync(DA).tif"
Model_FiLePath = r"E:yynctryedatamodel1.pickle"
Save_FilePath = r"E:yynctryedataresult_KNN.tif"

image1 = image_open(Image_FilePath)
width = image1.RasterXSize
height = image1.RasterYSize
Projection = image1.GetProjection()
Transform = image1.GetGeoTransform()
image2 = image1.ReadAsArray()

# 打开模型
model1 = model_open(Model_FiLePath)

# 在与测试前要调整一下数据的格式
data = np.zeros((image2.shape[0], image2.shape[1] * image2.shape[2]))
for i in range(image2.shape[0]):
    data[i] = image2[i].flatten()
data = data.swapaxes(0, 1)

# 对调整好格式的数据进行预测
pred = model1.predict(data)

# 同样地，我们对预测好的数据调整为我们图像的格式
pred = pred.reshape(image2.shape[1], image2.shape[2]) * 255
pred = pred.astype(np.uint8)

# 将结果写到tif图像里
writeTiff(pred, Transform, Projection, Save_FilePath)
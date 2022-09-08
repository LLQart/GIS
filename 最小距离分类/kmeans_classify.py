# coding:utf-8
import numpy as np
from osgeo import gdal



def readTiff(file):
    dataset = gdal.Open(file, gdal.GA_ReadOnly)
    im_bands = dataset.RasterCount
    # print(im_bands)
    im_width = dataset.RasterXSize
    im_height = dataset.RasterYSize
    im_data = dataset.ReadAsArray()
    # im_data = im_data.ReadAsArray()
    # print(im_data)
    return dataset, im_data

def writeTIff(dataset,im_data,path):
    im_proj = dataset.GetProjection()
    im_geotrans = dataset.GetGeoTransform()

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape
    driver = gdal.GetDriverByName("GTiff")
    new_dataset = driver.Create(path, im_width, im_height, im_bands, gdal.GDT_Float64)

    new_dataset.SetGeoTransform(im_geotrans)
    new_dataset.SetProjection(im_proj)

    if new_dataset != None:
        new_dataset.SetGeoTransform(im_geotrans)
        new_dataset.SetProjection(im_proj)

    if im_bands == 1:
        new_dataset.GetRasterBand(1).WriteArray(im_data)
    else:
        for i in range(im_bands):
            new_dataset.GetRasterBand(i+1).WriteArray(im_data[i])
    del new_dataset


def getPostions(roitif):
    dataset, im_data = readTiff(roitif)
    print(im_data.shape)
    im_band, im_height, im_width = im_data.shape

    maxValue = im_data.max()

    positions = [[] for i in range(maxValue)]

    for i in range(im_height):
        for j in range(im_width):
            value = im_data[i][j]
            if value != 0:
                pos = [i,j]
                positions[value-1].append(pos)
    return positions


def getCenters(roitif, im_data):
    positions = getPostions(roitif)
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape

    centers = []

    c_num = len(positions)

    for i in range(c_num):
        per_c = []
        perClassPos = positions[i]
        length = len(perClassPos)

        if im_bands == 1:
            sum = 0
            for m in range(length):
                pos = perClassPos[m]
                x, y = pos[0], pos[1]
                sum += im_data[x][y]
            mean = sum/length
            per_c.append(mean)
        else:
            for j in range(im_bands):
                sum = 0
                for m in range(length):
                    pos = perClassPos[m]
                    x, y = pos[0], pos[1]
                    sum += im_data[j][x][y]
                mean = sum / length
                per_c.append(mean)
        centers.append(per_c)
    return centers

def changeData(im_data):
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape

    empty = np.zeros((im_height, im_width))
    data = np.zeros((im_height*im_width, im_bands))
    if im_bands == 1:
        for i in range(im_height):
            for j in range(im_width):
                data[i*im_width+j][0] = im_data[i][j]
    else:
        for m in range(im_bands):
            for i in range(im_height):
                for j in range(im_width):
                    data[i*im_width+j][m] = im_data[m][i][j]
    return data, empty

def classification(im_data,centers):
    data, empty = changeData(im_data)
    centers = np.array(centers)
    length = centers.shape[0]

    height, width = empty.shape
    for i in range(data.shape[0]):
        per_data = data[i]
        diffMat = np.tile(per_data, (length, 1)) - centers

        sqDiffMat = diffMat ** 2
        sqlDisMat = sqDiffMat.sum(axis=1)

        sortedIndex = sqlDisMat.argsort()

        h = i // width
        w = i - h*width
        empty[h][w] = sortedIndex[0]

    return empty

if __name__ == '__main__':
    dataset, im_data = readTiff(r"D:\workspace\images\LC81200382020275LGN00\flaashed.tif")
    print(im_data)
    centers = getCenters(r"D:\workspace\images\LC81200382020275LGN00\ROI.tif", im_data)
    print(centers)
    empty = classification(im_data, centers)
    print('empty', empty)
    writeTIff(dataset, empty, r"D:\workspace\images\LC81200382020275LGN00\classify.tif")
    print("classified successful!")

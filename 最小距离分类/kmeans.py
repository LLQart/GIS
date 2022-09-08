# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
import xlrd

color_list = ["yellow", "red", "green", "purple", "black"]

def classify(data, centers):
    length = centers.shape[0]

    classes = [ [] for i in range(length) ]

    sumDis = 0
    for i in range(data.shape[0]):
        per_data = data[i]
        diffMat = np.tile(per_data, (length,1)) - centers
        sqlDiffMat = diffMat**2
        sqlDisMat = sqlDiffMat.sum(axis=1)  # axis=0为按列求和  1为按行求和
        sortedIndex = sqlDisMat.argsort()  # 按照索引排序
        classes[sortedIndex[0]].append(list(per_data))  # 将数据添加到分类里面
        sumDis += sortedIndex[0]

    return classes, sumDis

def upCenters(classes):
    newCenters = []
    for i in range(len(classes)):
        per_class = classes[i]  # list
        per_class = np.array(per_class)  # 列表不能按列求和，所以转为数组
        center = per_class.sum(axis=0)/len(per_class)
        newCenters.append(center)
    return np.array(newCenters)



def kmeans(data, centers, sumDis):
    """
    :param data:
    :param centers:
    :param sumDis:
    :return:
    """
    # 聚类
    classes, new_sumDis = classify(data, centers)

    if sumDis == new_sumDis:
        return
    # 修改中心点
    newCenters = upCenters(classes)

    # 画图
    for i in range(len(newCenters)):
        center = centers[i]
        plt.scatter(center[0], center[1], s = 8*np.pi**2, marker="*", c=color_list[i])

    for i in range(len((classes))):
        per_class = classes[i]
        for c in per_class:
            plt.scatter(c[0], c[1], c=color_list[i])
    plt.title("sumDistance%f"%new_sumDis)

    kmeans(data, newCenters, new_sumDis)
    # 再聚类
    # 再修改中心点
    # 两次总的距离一致就停止

def getData(xlsx):
    workbook = xlrd.open_workbook(xlsx)
    worksheet = workbook.sheet_by_index(0)
    nrows, ncols = worksheet.nrows, worksheet.ncols

    data = []

    for i in range(nrows):
        temp = []
        for j in range(ncols):
            temp.append(worksheet.cell_value((i,j)))
        data.append(temp)

    return np.array(data)

if __name__ == '__main__':
    xlsx = r""
    data = getData(xlsx)
    centers = data[:3]
    kmeans(data, centers, 0)
    plt.show()


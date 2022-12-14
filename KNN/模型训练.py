from sklearn import neighbors
import numpy as np
from sklearn import model_selection
import pickle


# 定义字典，便于来解析样本数据集txt
def Iris_label(s):
    it = {b'no-lodging': 0, b'Lodging': 1}
    return it[s]


path = r"E:yynctryedatadata.txt"
SavePath = r"E:yynctryedatamodel1.pickle"

# 读取数据集
data = np.loadtxt(path, dtype=float, delimiter=',', converters={4: Iris_label})
#  converters={4:Iris_label}中“4”指的是第5列：将第5列的str转化为label(number)

# 划分数据与标签
x, y = np.split(data, indices_or_sections=(4,), axis=1)  # x为数据，y为标签
x = x[:, 0:4]  # 选取前4个波段作为特征
train_data, test_data, train_label, test_label = model_selection.train_test_split(x, y, random_state=1, train_size=0.9,
                                                                                  test_size=0.1)

# 用K=1的参数，训练KNN模型(调参)
classifier = neighbors.KNeighborsClassifier(n_neighbors=1)
classifier.fit(train_data, train_label.ravel())  # ravel函数拉伸到一维

# 计算随机森林的准确率
print("训练集：", classifier.score(train_data, train_label))
print("测试集：", classifier.score(test_data, test_label))

# 保存模型
# 以二进制的方式打开文件：
file = open(SavePath, "wb")
# 将模型写入文件：
pickle.dump(classifier, file)
# 最后关闭文件：
file.close()

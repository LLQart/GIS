from sklearn import neighbors
import numpy as np
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt


# 定义字典，便于来解析样本数据集txt
def Iris_label(s):
    it = {b'no-lodging': 0, b'Lodging': 1}
    return it[s]


Path = r"E:yynctryedatadata.txt"

# 读取数据集
data = np.loadtxt(Path, dtype=float, delimiter=',', converters={4: Iris_label})
#  converters={4:Iris_label}中“4”指的是第5列：将第5列的str转化为label(number)

# 划分数据与标签
x, y = np.split(data, indices_or_sections=(4,), axis=1)  # x为数据，y为标签

# 利用十折交叉验证，搜索K值于1至30处的误差
K_range = range(1, 30)
K_error = []
for i in K_range:
    KNN = neighbors.KNeighborsClassifier(n_neighbors=i)
    scores = cross_val_score(KNN, x, y.ravel(), cv=10, scoring="accuracy")
    K_error.append(scores.mean())

# 绘制不同K值的误差曲线图
plt.plot(K_range, K_error, color="pink")
plt.xlabel("K value")
plt.ylabel("Accuracy")
plt.grid(ls="--", c="gainsboro")
plt.show()
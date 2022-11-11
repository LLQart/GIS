# 清洗高德地图上的地铁线路数据

#### 介绍
主要用于清洗从高德地图搜索得到的地铁线路数据并生成SHP文件和GeoJSON文件，涵盖了高德坐标系、百度坐标系和WGS1984坐标系三种类型的坐标点数据，方便在不同地图平台上使用。
该版本实验数据根据百度百科搜索的地铁线路名称进行搜索得到，暂时无法确保已经将所有线路数据全部获取并清洗成功。

**实际使用数据仍需使用者再次核实验证。**

#### 依赖的第三方库

| 序号 | 第三方库                     | 用途               |
|----|--------------------------|------------------|
| 1  | os                       | 文件读写             |
| 2  | json                     | JSON文件处理         |
| 3  | math                     | 坐标点转换            |
| 4  | Feature,Point,LineString | geojson原始数据处理    |
| 5  | FeatureCollection        | geojson数据汇总      |
| 6  | shapefile                | shapefile文件处理    |
| 7  | osr                      | shapefile文件坐标系处理 |
| 8  | geopandas                | geojson数据快速处理 |

#### 文件夹整理
整个项目文件目录如下

![](https://images.gitee.com/uploads/images/2021/0217/221540_4fc382fb_7654995.png "项目文件目录.png")

#### 数据搜集过程
在高德地图网页端搜索目标城市的地铁线路（运营中和在建线路名称），按下 ***F12*** 查看查询后返回的数据内容。
![](https://images.gitee.com/uploads/images/2021/0217/222434_2dd62613_7654995.png "屏幕截图.png")

将返回的JSON数据复制保存到相应城市的JSON文件夹下。

![](https://images.gitee.com/uploads/images/2021/0217/222638_e38def9b_7654995.png "屏幕截图.png")

**这将是一件比较枯燥的工作，有部分城市在建的地铁线路与百度百科找到的线路无法对应。**


#### 清洗整理得到高德坐标系的SHP文件和GeoJSON文件
打开一级目录下的 ***_01_GetSubwayGeoInfo.py*** 程序，程序将自动完成数据转换

#### 转换得到百度坐标系/WGS1984坐标系SHP文件和GeoJSON文件
打开一级目录下的 ***_02_EditCoor_.py*** 程序，设定
- 文件类型（SHP/GeoJSON）
- 形状类型（线路/站点）
- 坐标系名称（baidu/wgs84）

至此，高德地图获取的地铁线路数据站点/线路，高德坐标系、百度坐标系、WGS1984坐标系的数据都已全部清洗整理完毕。

#### 成果展示
![](https://images.gitee.com/uploads/images/2021/0218/155004_c1719337_7654995.jpeg "subway_output(1).jpg")
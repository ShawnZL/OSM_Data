# 使用说明

## ways_Origin.csv

`ways.csv`：在  `(south west north east)`  -> `(0, 98, 27, 123.422)` 范围内的所有海航线路径汇总。

格式为`(Num, id, nodes, start, end, distance)` -> `(序号，航线id，经过坐标点序列，起点，终点，距离)`，其中所有 `node` 的格式为`(id, lat经度, lon纬度)`

## ways_Order.csv

将 `ways_Origin.csv` 中的数据按照num递增的顺序增加

## nodes_Origin.json

`{"id":"", "lat":"", "lon":""}` 形式

航路节点中所有节点的原始数据。没有经过处理，会有很多数据出现重复现象

## nodes1.json

将原始数据`nodes_Origin.json`中重复节点都删除

## nodes_China.json

将`nodes1.json`中节点数据，根据高德地图API判断是否是在国内

## 

## OSM的API使用

### Overpass API

[Python Overpass API文档](https://python-overpy.readthedocs.io/en/latest/api.html#overpy.Way.get_nodes)

[官方文档](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Bounding_box)

其中对于API文档调用范围，需要严格注意！

[Example](https://supergis.gitbooks.io/git_notebook/content/doc/osm-overpass-node.html)
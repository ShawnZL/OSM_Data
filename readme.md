# 使用说明

## nodes.json

`nodes.json`:所有节点ID + 经纬度

## ways.csv

`ways.csv`：在  `(south west north east)`  -> `(0, 98, 27, 123.422)` 范围内的所有海航线路径汇总。

格式为`(Num, id, nodes, start, end, distance)` -> `(序号，航线id，经过坐标点序列，起点，终点，距离)`，其中所有 `node` 的格式为`(id, lat经度, lon纬度)`
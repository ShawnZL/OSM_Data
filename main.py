import glob
import time
import json
import overpy
import csv
import pandas as pd
def print_hi():
    api = overpy.Overpass()
    #纬度1 经度1 纬度2 经度2
    #south west north east
    result = api.query("node(8.9294,113.4979,9.8547,112.4817);out;")
    #result = api.query("[out:json];node(8.9294,113.4979,9.8547,112.4817);out;")
    #print(len(result.nodes))
    print(len(result.ways))

def node2json(node):
    jsonNode="{\"id\":\"%s\", \"lat\":\"%s\", \"lon\":\"%s\"}"%(node.id,node.lat,node.lon)
    return jsonNode

#将节点转换为list 形式存储[id, lat, lon]
def node2list(node):
    nodelist=[node.id, float(node.lat), float(node.lon)]
    return nodelist

def node2jsonfile(fname,nodeset,number):
    fnode = open(fname,"a") #w是覆盖写，a是追加写
    for n in nodeset:
        jn = node2json(n) + "\n"
        fnode.write(jn)
    fnode.close()
    print("Num:", number, " Nodes: ", len(nodeset), " Write to: ", fname)

def get_way():
    api = overpy.Overpass()
    # south west north east
    result = api.query("""way["route"="ferry"](0, 98, 27, 123.422);out;""")
    print(len(result.ways))
    print("Way1: ", result.ways[0])
    nodes = []
    nodest = result.ways[0].get_nodes(resolve_missing=True)
    for n in nodest:
        templist = node2list(n)
        nodes.append(templist)
    #Try to resolve missing nodes. return List[]
    print(nodes)
    print(nodes[0])
    print(nodes[-1])
    #print(result.ways[0].id)
    #print(result.ways[0].get_nodes(resolve_missing=True))
    #print("Way2: ", result.ways[1])


def get_waysAnodes():
    api = overpy.Overpass()
    # south west north east
    result = api.query("""way["route"="ferry"](0, 98, 27, 123.422);out;""")
    #print(len(result.ways))
    length = len(result.ways)
    for i in range(7, length):
        nodes = result.ways[i].get_nodes(resolve_missing=True)
        node2jsonfile("node.json", nodes)
    #nodes = result.ways[0].get_nodes(resolve_missing=True)
    #print(nodes[0].id)
    #print(nodes[0].lat)
    #print(nodes[0].lon)

def get_node():
    api = overpy.Overpass()
    result = api.query("node(0, 98, 27, 123.422);out;")
    print(len(result.nodes()))
    print(result.nodes[0:3])

def get_way2csv():
    api = overpy.Overpass()
    # south west north east
    result = api.query("""way["route"="ferry"](0, 98, 27, 123.422);out;""")
    print(len(result.ways))
    length = len(result.ways)
    f = open('ways.csv', 'a', encoding='utf-8')
    writer = csv.writer(f)
    #writer.writerow(["id", "nodes", "start", "end", "distance"])
    for i in range(0, 10):
        nodes = []  # 存储节点
        nodest = result.ways[i].get_nodes(resolve_missing=True)
        node2jsonfile('nodes14.json', nodest)
        for n in nodest:
            templist = node2list(n)
            nodes.append(templist)
        writer.writerow([result.ways[i].id, nodes, nodes[0], nodes[-1]])
        time.sleep(3)
    # print(type(result.ways[0]))
    # print(result.ways[0].id)
    # print("Way2: ", result.ways[1])

def get_way2csv2():
    api = overpy.Overpass()
    # south west north east
    result = api.query("""way["route"="ferry"](0, 98, 27, 123.422);out;""")
    print(len(result.ways))
    length = len(result.ways)
    f = open('ways.csv', 'a', encoding='utf-8')
    f1 = open('error.txt', 'a', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(["Num", "id", "nodes", "start", "end", "distance"])
    for i in range(540, 541):
        nodes = []  # 存储节点
        try:
            nodest = result.ways[i].get_nodes(resolve_missing=True)
        except BaseException:
            print("error: ", i)
            strtemp = str(i) + '\n'
            f1.write(strtemp)
            i -= 1
            time.sleep(10)
        else:
            node2jsonfile('nodes1.json', nodest, i)
            for n in nodest:
                templist = node2list(n)
                nodes.append(templist)
            writer.writerow([i, result.ways[i].id, nodes, nodes[0], nodes[-1]])
            time.sleep(3)
    # print(type(result.ways[0]))
    # print(result.ways[0].id)
    # print("Way2: ", result.ways[1])

def ways2res():
    api = overpy.Overpass()
    # south west north east
    result = api.query("""way["route"="ferry"](0, 98, 27, 123.422);out;""")
    print(len(result.ways))
    length = len(result.ways)
    f = open('ways.csv', 'a', encoding='utf-8')
    f1 = open('error1.txt', 'a', encoding='utf-8')
    writer = csv.writer(f)
    with open("error.txt", 'r') as f2:
        for line in f2.readlines():
            #line = line.strip('\n') #去掉列表中每一个元素的换行符号
            print(line)
            num = int(line)
            nodes = []  # 存储节点
            try:
                nodest = result.ways[num].get_nodes(resolve_missing=True)
            except BaseException:
                print("error: ", num)
                strtemp = str(num) + '\n'
                f1.write(strtemp)
                time.sleep(10)
            else:
                node2jsonfile('nodes1.json', nodest, num)
                for n in nodest:
                    templist = node2list(n)
                    nodes.append(templist)
                writer.writerow([num, result.ways[num].id, nodes, nodes[0], nodes[-1]])
            time.sleep(3)

# 按照Num对数据进行排序
def order_csv():
    df = pd.read_csv('ways.csv')
    data = df.sort_values(by="Num", ascending = True)  #升序
    data.to_csv('way1.csv', index = False)
#去除双引号
def rm_csv():
    pd.read_csv('way1.csv', usecols=['nodes', 'start', 'end']).to_csv('way2.csv', quoting=csv.QUOTE_NONE, index=False)

def merge_JsonFiles():
    reslut = []
    for f in glob.glob("*.json"):
        with open(f, "rb") as infile:
            reslut.append(json.load(infile))
    with open("merged_file.json", "wb") as outfile:
        json.dump(reslut, outfile)


if __name__ == '__main__':
    #get_way()
    #get_waysAnodes()
    #get_node()
    #get_way2csv2()
    #get_temp()
    #ways2res()
    #order_csv()
    merge_JsonFiles()

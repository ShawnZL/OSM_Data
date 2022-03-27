import glob
import time
import json
import overpy
import csv
import pandas as pd
import requests

AK = ''
key = ''

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

#合并Json文件
def merge_JsonFiles():
    reslut = []
    for f in glob.glob("*.json"):
        with open(f, "rb") as infile:
            reslut.append(json.load(infile))
    with open("merged_file.json", "wb") as outfile:
        json.dump(reslut, outfile)

# 根据高德API判断点是否在国界内
def Gaode_Nodes(location):
    #location = '123.46673,25.74783'
    url = 'https://restapi.amap.com/v3/geocode/regeo?output=json&location=%s&key=%s&radius=0&extensions=all'%(location,key)
    res = requests.get(url)

    if res.status_code == 200:
        val = res.json() #解读为Json
        if val['status'] == '1':
            temp_pro = val['regeocode']['addressComponent']['province']
            temp_con = val['regeocode']['addressComponent']['country']
            #temp_seaArea = val['regeocode']['addressComponent']['seaArea']
            if (temp_con == '中国' or temp_pro == '中华人民共和国'):
                print(4)
                return True
    else:
        print('无法获取%s位置信息' % location)
    return False

#处理Json文件，只保留一个节点，
def Deal_Node():
    #将重复节点删除
    """
    js = open('nodes.json', 'r')
    f1 = open('nodes1.json', 'a')
    cont = js.readlines() #将Json读取
    length = len(cont)
    node_dic = {}
    for i in range(0, length):
        temp = cont[i]
        res = json.loads(temp)

        if (node_dic.get(res['id']) == None):
            node_dic[res['id']] = 1
            js = cont[i]
            f1.write(js)
        else:
            print('已经存在')
    """
    f1 = open('nodes11.json', 'r')
    f2 = open('nodes2.json', 'a')
    cont = f1.readlines()
    length = len(cont)
    flag = 0
    for i in range(0, length):
        res = json.loads(cont[i])
        loaction = res['lon'] + ',' + res['lat']
        if Gaode_Nodes(loaction):
            print(i, ":1")
            f2.write(cont[i])
            flag += 1
        else:
            print(i, ":2")
    print(flag)

#将CSV文件转换为Json
def CSV2Json():
    data = pd.read_csv('ways2.csv', encoding='utf-8')
    f1 = open('ways.json', 'a')
    length = len(data)
    #for i in range(0, length):


#将所有路径中国内的节点保存下来，转为csv形式
def Deal_CSV():
    data = pd.read_csv('ways_Order.csv', encoding='utf-8')
    f_test = open('temp.csv', 'a')
    f1 = open('nodes_China.json', 'r')
    f2 = open('SouthSea.csv', 'a')
    writer = csv.writer(f2)
    writer.writerow(["id", "nodes", "start", "end", "distance"])
    ######################
    nodes_dic = {} # 将所有节点读进字典中
    cont = f1.readlines() #读取所有数据
    length = len(cont)
    for i in range(0, length):
        res = json.loads(cont[i]) #转换为json
        nodes_dic[res['id']] = 1
    #####################
    length2 = len(data)
    """
    temp_str = data.iloc[0]['nodes']
    res = json.loads(temp_str) #加载完Json形式
    print(len(res))
    print(type(res[0]))
    ans = []
    for i in range(0, len(res)):
        if dic.get(str(res[i][0])) == 1:
            ans.append(res[i])
    print(ans)
    temp_record = data.iloc[0]
    temp_record['nodes'] = ans
    print(temp_record['nodes'])
    """
    for i in range(0, length2):
        temp_str = data.iloc[i]['nodes'] #获取每一行的nodes
        res = json.loads(temp_str) #加载为Json形式
        ans = []
        for j in range(0, len(res)):
            if nodes_dic.get(str(res[j][0])) == 1:
                ans.append(res[j])
        print(data.loc[i]['id'])
        print(ans)
        print(data.loc[i]['start'])
        data.loc[i]['end']
        if ans != []:
            writer.writerow([data.loc[i]['id'], ans, data.loc[i]['start'], data.loc[i]['end']])
            print(len(ans))
            print(len(res))
        print('###################')


if __name__ == '__main__':
    #get_way()
    #get_waysAnodes()
    #get_node()
    #get_way2csv2()
    #get_temp()
    #ways2res()
    #order_csv()
    #Gaode_Nodes()
    Deal_CSV()


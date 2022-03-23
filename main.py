import overpy
import csv

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

def node2jsonfile(fname,nodeset):
    fnode = open(fname,"a") #w是覆盖写，a是追加写
    for n in nodeset:
        jn = node2json(n) + "\n"
        fnode.write(jn)
    fnode.close()
    print("Nodes:",len(nodeset),", Write to: ",fname)

def get_way():
    api = overpy.Overpass()
    # south west north east
    result = api.query("""way["route"="ferry"](0, 98, 27, 123.422);out;""")
    print(len(result.ways))
    print("Way1: ", result.ways[0])
    nodes = []
    nodes = result.ways[0].get_nodes(resolve_missing=False)
    #Try to resolve missing nodes. return List[]
    print(nodes)
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
    writer.writerow(["id","nodes"])
    for i in range(1, 5):
        nodes = result.ways[i].get_nodes(resolve_missing=True)
        node2jsonfile("node1.json", nodes)
        writer.writerow([result.ways[i].id, nodes])
    # print(type(result.ways[0]))
    # print(result.ways[0].id)
    # print("Way2: ", result.ways[1])

if __name__ == '__main__':
    #get_way()
    #get_waysAnodes()
    #get_node()
    get_way2csv()


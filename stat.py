import pandas as pd

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def create_graph(filename):
    G1 = nx.Graph()
    df = pd.read_csv(filename)
    for row in df.values:
            G1.add_edge(row[0], row[5])

    # pos = nx.circular_layout(G1)
    # nx.draw(G,with_labels=True, arrows=True, node_size=700)
    # nx.draw(G1, pos, with_labels=True,node_size=200)
    # nx.draw(G1, with_labels=True,node_size=200)
    # plt.show()
    return G1

# G=create_graph('consolidated_csv/fragments_ds100_dt300.csv')

# def statistice(G):



# 0.9638707755094332

setting={0:'ds100_dt300',1:'ds500_dt600',2:'ds1000_dt1200'}

# def statistice(G):
print(setting.values())
lconn=[]
def get_largest_connected_component(G_list):
    for idx, graph in enumerate(G_list):
        larg_graph=nx.Graph()
        print("Largest Connected component for "+str(setting.get(idx)))
        print(len(max(nx.connected_components(graph))))
        larg_graph.add_path(max(nx.connected_components(graph), key=len))
        plt.title(str(setting.get(idx))  +'\n length='+str(len(max(nx.connected_components(graph)))))

        nx.draw(larg_graph, with_labels=True)
        plt.show()
        plt.close()



        lconn.append(len(max(nx.connected_components(graph))))
    plt.ylabel("Length of connected components")
    plt.xlabel("Settings")

    plt.plot(setting.values(), lconn)
    plt.savefig('figures/larg_conn_comp.png')
    plt.show()


avg_deg=[]
def get_average_degree(G_list):
    for idx, graph in enumerate(G_list):
        d1 = []
        for i in list(graph.nodes):
            d1.append(graph.degree[i])
        print("Average degree for "+str(setting.get(idx)))
        print(np.array(d1).mean())
        avg_deg.append(np.array(d1).mean())
    plt.ylabel("Degrees")
    plt.xlabel("Settings")
    plt.plot(setting.values(), avg_deg)
    plt.savefig('figures/average_degree.png')

    plt.show()




list_of_files=['consolidated_csv/fragments_ds100_dt300.csv','consolidated_csv/fragments_ds500_dt600.csv','consolidated_csv/fragments_ds1000_dt1200.csv']
Graph_List=[]
for filename in list_of_files:
    G = create_graph(filename)
    Graph_List.append(G)

print(len(Graph_List))

get_largest_connected_component(Graph_List)
get_average_degree(Graph_List)









import itertools, networkx as nx, matplotlib.pyplot as plt

koordinate = [(1,1), (1,5), (2,3), (5,0)]

def graf(koordinate):
    G = nx.Graph()
    i = 0
    for par in koordinate:
        G.add_node(i, pos = par)
        i += 1
    robovi = itertools.combinations([j for j in range(i)], 2)
    G.add_edges_from(robovi)
    nx.draw(G)
    plt.show()
    return nx.edges(G)

graf(koordinate)

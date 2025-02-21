'''
CECS 427 Project 2
Date: February 21, 2025
Written by: Chi Vo

'''

import matplotlib.pyplot as plt
import networkx as nx
import argparse
import fractions

isComponents = False

''' FUNCTIONS '''

def BFS(G, startNode):
    
    newG = nx.Graph()
    shortest_paths_data = dict(nx.single_source_all_shortest_paths(G, startNode))
    paths = list(shortest_paths_data.values())

    path_list = []

    for i in paths:
        for j in range(len(i)):
            if len(i[j]) > 1:
                path_list.append(i[j])

    for j in path_list:
        nx.add_path(newG, j)

    
    pos = nx.bfs_layout(newG, startNode)

    nx.draw_networkx(newG, pos=pos, with_labels=True, font_size=9, node_size=255, font_color='#ffffff', arrows=False)
    plt.title(f"BFS Tree starting from node {startNode}")
    plt.show()



def components(G, n):
    C = nx.community.edge_betweenness_partition(G, n)

    if C != None: # if there are n components, divides G into n subgraphs
        G_old = G
        G = nx.Graph()

        for a_set in C:

            subG = G_old.subgraph(a_set)
            G.add_nodes_from(subG.nodes)
            G.add_edges_from(subG.edges)
    
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos=pos, with_labels=True, font_size=9, node_size=260, font_color='#ffffff')
    plt.title(f"Graph partitioned to {n} connected component(s)")
    plt.show()

    return C # a list of partitions of the nodes of G


def plot(G, choice, C=None):

    if 'C' in choice:

        G_new = nx.Graph()
        if C != None:
            length = len(C)
        else: length=1

        for i in range(length):
            if C != None:
                subgraph = G.subgraph(C[i])
            else: subgraph = G    
            cc = nx.clustering(subgraph)
            print(f"Clustering coefficients for subgraph {i+1}: {cc}\n")
            cluster_min = 0
            cluster_max = 1

            max_pixel = 700
            min_pixel = 100

            degrees = [val for (node, val) in G.degree()]
            d_max = max(degrees)


            for node in list(subgraph.nodes):
                c_v = nx.clustering(G, node)
                p_v = (c_v - cluster_min) / (cluster_max - cluster_min)
                v_node_size = min_pixel + p_v * (max_pixel - min_pixel)
                
                d_v = subgraph.degree[node]
                s_v = d_v / d_max
                v_color = ((254*s_v/254), 0//254, 254//254)

                G_new.add_node(node, size=v_node_size, color=v_color)
                
            G_new.add_edges_from(subgraph.edges())

        pos = nx.spring_layout(G_new)
        nx.draw_networkx(G_new, pos=pos, node_color=[G_new.nodes[node]['color'] for node in G.nodes()], 
                    node_size=[G_new.nodes[node]['size'] for node in G.nodes()], with_labels=True, font_size=8, font_color='#FFFF00', font_weight='bold')
        plt.title("Graph with highlighted clustering coefficient")
        plt.show()


    if 'N' in choice:
        for i in G.edges():
            common_neighbors = list(nx.common_neighbors(G, i[0], i[1]))
            neighbor_one = list(G.neighbors(i[0]))
            neighbor_two = list(G.neighbors(i[1]))
            
            for j in common_neighbors:
                neighbor_one.remove(j)
                neighbor_two.remove(j)

            neighborhood_overlap = fractions.Fraction(len(common_neighbors), len(common_neighbors)+len(neighbor_one)+len(neighbor_two))
            print(f"Neighborhood overlap of Edge {i}: {neighborhood_overlap}")

            G.add_edge(i[0], i[1], neighborhood_overlap=str(neighborhood_overlap))
        
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos=pos, with_labels=True, font_size=8, font_color='#FFFFFF', font_weight='bold')
        edge_labels = nx.get_edge_attributes(G, "neighborhood_overlap")
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7)


        def onclick(event,pos=pos):
            if event.xdata is not None and event.ydata is not None:
                for node, (x, y) in pos.items():
                    # Check if the click is within a certain radius of the node
                    if (event.xdata - x)**2 + (event.ydata - y)**2 <= 0.01:  # Adjust radius as needed
                        print(f"Clicked on node: {node}")

                        plt.figure()
                        BFS(G, node)
                        
                        break

        # Connect the click event to the function
        plt.gcf().canvas.mpl_connect('button_press_event', onclick)

        plt.title("Graph with neighborhood overlap ratio")
        plt.show()



    if 'P' in choice:
        pos = nx.spring_layout(G)
        for i in G.nodes():
            if "color" in G.nodes[i].keys():
                nx.draw_networkx(G, pos=pos, with_labels=True, font_size=8, node_size=260, font_color='#ffffff', node_color=[G.nodes[node]['color'] for node in G.nodes()])
            else:
                nx.draw_networkx(G, pos=pos, with_labels=True, font_size=8, node_size=260, font_color='#ffffff')
        plt.title("Graph plotting")
        plt.show()


def verify_homophily(G):
    # p -> red nodes; q (or 1-p) -> green nodes
    cross_colored_edges = 0
    res = False

    number_of_nodes = len(list(G.nodes()))
    number_of_edges = len(list(G.edges()))
    number_of_red_nodes, number_of_green_nodes = 0, 0
    for j in G.nodes():
        if G.nodes[j]['color'] == "r":
            number_of_red_nodes += 1
            for i in G.neighbors(j):
                if G.nodes[i]['color'] == "g":
                    cross_colored_edges += 1
        else: number_of_green_nodes += 1
    p = fractions.Fraction(number_of_red_nodes, number_of_nodes)
    a = fractions.Fraction(cross_colored_edges, number_of_edges)
    mu = 2*p*(1-p)


    if a < mu: 
        res = True
    
    return res, a, mu



def verify_balanced_graph(G):
    cycles = nx.cycle_basis(G)
    cycle_edges = [list([(cycle[i], cycle[i+1]) for i in range(len(cycle)-1)] + [(cycle[-1], cycle[0])]) for cycle in cycles]

    isBalanced = True
    for cycle in cycle_edges:
        number_of_neg_signs = 0
        for edge in cycle:
            if G.edges[edge]['sign'] == '-':
                number_of_neg_signs += 1
        if number_of_neg_signs % 2 != 0:
            isBalanced = False

    return isBalanced




def output(G, outputFile):
    nx.write_gml(G, outputFile)



''' MAIN CODE '''

parser = argparse.ArgumentParser(prog="graph_analysis")

parser.add_argument("inputfile", type=str)
parser.add_argument("--components", type=int)
parser.add_argument("--plot", type=str, help='C: clustering coefficients; N: neighborhood overlap; P: color the nodes')
# parser.add_argument("--plot", action="store_true")
parser.add_argument("--verify_homophily", action="store_true")
parser.add_argument("--verify_balanced_graph", action="store_true")
parser.add_argument("--output", type=str)


args = parser.parse_args()


if args.inputfile:
    inputFile = args.inputfile
    G = nx.read_gml(inputFile) # read the graph from the input .gml file

if args.components:
    n = args.components
    C = components(G, n)
else:
    C = None  

if args.plot:
    userChoice = args.plot

    # if there are n components, divides G into n subgraphs
    if C != None:
        G_old = G
        G = nx.Graph()

        for a_set in C:

            subG = G_old.subgraph(a_set)
            G.add_nodes_from(subG.nodes)
            G.add_edges_from(subG.edges)

        plot(G, userChoice, C)
    else: 
        plot(G, userChoice)


if args.verify_homophily:
    if C != None:
        isHomophily, a, mu = verify_homophily(G_old)
    else:
        isHomophily, a, mu = verify_homophily(G)

    if isHomophily:
        print(f"Graph exists evidence of homophily:\na={a}    <   μ={mu}")
    else:
        print(f"Graph DOES NOT exist evidence of homophily\na={a}    >=   μ={mu}")
    


if args.verify_balanced_graph:
    if verify_balanced_graph(G):
        print("Graph is balanced.")
    else:
        print("Graph is not balanced.")


if args.output:
    outputFile = args.output
    output(G, outputFile)

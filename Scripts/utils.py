import pandas as pd
import networkx as nx
from libpysal.weights import Queen
from scipy.spatial.distance import cdist
import igraph as ig


# Production information columns of the data
columns = ['11', '21', '22', '23', '31-33', '43', '46',
           '48-49', '51', '52', '53', '54', '55', '56',
           '61', '62', '71', '72', '81']


def create_graph_networkx(geo):
    """
    Creates a adjacency networkx graph based on a .gpkg file
    where the index is the name of the entities

    Returns:
        Networkx graph
        adj matrix of the graph
    """

    # Calculate adjacency matrix
    weights = Queen.from_dataframe(geo, use_index=True)
    adj_matrix = weights.full()[0]
    # Create graph from adj matrix
    G = nx.from_numpy_array(adj_matrix)

    # Relabel vertex names with the index values
    id_mun = geo.index
    id_dict ={i: id_ for i, id_ in enumerate(id_mun)}
    G = nx.relabel_nodes(G, id_dict)

    return G, adj_matrix


def get_instance_information(G, adj_matrix, geo, distance='cityblock'):
    """
    Based on the adjacency graph and .gpkg file, get relevant information of the instance

        Returns:
        N - Number of nodes
        V - List of nodes
        NB - List of neighbors
        D - Distance matrix
    """
    # Number of nodes
    N = len(G.nodes())  
    # List of nodes
    V = list(G.nodes()) 

    # List of neighbors
    NB = [list(G.neighbors(node)) for node in G.nodes]

    # Distance matrix
    distances = cdist(geo[columns], geo[columns], metric=distance)
    D = pd.DataFrame(distances, index=geo.index, columns=geo.index) 
    return N, V, NB, D


def get_p_from_n(n):
    """
    Get the number of regions of an instance based on the size

    Returns:
        List of p (number of regions) for that instance
    """
    if n < 20:
        return [3, 5, 7]
    elif n <60:
        return [5, 7, 10]
    else:
        return [10, 15, 20]



def Create_Instance_Flow(N, V, NB, D, p, output_file):
    """
    Creates a flow instance in a .txt file 

    Input:
        N - Number of nodes
        V - List of nodes
        NB - List of neighbors
        D - Distance matrix
        p - Number of regions
        output_file - outputfile to save the instance (.txt)        
    """

    # open the file to write the instance
    instance = open(output_file, 'w')
   
    # Write number and set of areas
    output = '!n: Number of areas\n'
    output += f'n: {N}\n'
    output += '!I: Set if areas\n'
    output += 'I: [' + ' '.join(map(str, V)) + ' ]\n'

    # Write number and set of regions
    output += '!p: Number of regions\n'
    output += f'p: {p}\n'
    output += '!K: Set of regions\n'
    K = list(range(1, p+1))
    output += 'K: [' + ' '.join(map(str, K)) + ' ]\n'
       
    # Write Neighbors of each area
    output += '!N: Node Neighbor Set\n'
    output += 'N: [\n'
    for i, neighbors in zip(V, NB):
        neighbors_str = ' '.join(map(str, neighbors))
        output += f'({i}) [{neighbors_str}]\n'
    output += ']\n'
    
    # Write Distance matrix
    output += '!d(i,j): distance list\n'
    output += 'd: [\n'
    for i in D.index:
        for j in D.columns:
            output += f'({i} {j}) {D.loc[i,j]}\n'
    output += ']\n'
    
    # close file
    instance.write(output)    
    instance.close()



def get_igraph_graph(G_nx, geo):
    """
    Get a igraph graph representing adjacency,
    and with production vectors as node atribures

    Input: 
    G_nx - networkx graph representing adjacency
    geo - .gpkg file
    """

    # create an empty graph
    G = ig.Graph()
        
    # get list of edges from the nx graph
    edges = list(G_nx.edges)

    # add the vertices, a "name" atribute is created for each one
    vertices = list(set([v for edge in edges for v in edge]))        
    G.add_vertices(vertices) 
    # add edges
    G.add_edges(edges)

    # for each vector, get the production vector
    vectors = {}
    for v in G.vs["name"]:
        vectors[v] = geo.loc[v, columns].values
    # add production vectors as node atributes
    G.vs["x"] = list(vectors.values())

    return G
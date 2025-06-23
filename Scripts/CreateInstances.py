import geopandas as gpd
from utils import create_graph_networkx, get_instance_information
from utils import get_p_from_n,  Create_Instance_Flow, get_igraph_graph
from tqdm import tqdm
import os 

# Path to the procesed data
path = "../Data/Processed Data/"
# Output folders
flow_folder_path = "../Instances/Flow Instances/"
graph_folder_path = "../Instances/Graph Instances/"
GPKG_folder_path = "../Instances/GPKG Instances/"

# Create folders, if needed
os.makedirs(flow_folder_path, exist_ok=True)
os.makedirs(graph_folder_path, exist_ok=True)
os.makedirs(GPKG_folder_path, exist_ok=True)

"""_summary_
Use the processed data to create instances for each state:
    Creation of Flow instances.
    Creation of GPKG Instances
    Creation of igraph instances.
"""

# Read the processed data 
df = gpd.read_file(path + 'mun_ce19.gpkg')
df = df.set_index('CVEGEO')


# ---------------------------------------------------------------------
# Create instances for each state 1 - 32 
for i in tqdm(range(1,33)):
    ent = str(i).zfill(2)

    # Get the data for that state, and add x,y columns
    df_ent = df[df["CVE_ENT"] == ent]
    geo = df_ent.copy()
    geo["x"] = geo.centroid.x
    geo["y"] = geo.centroid.y

    # Save the .gpkg file of this state
    gpkg_filepath = GPKG_folder_path + f"{ent}.gpkg"
    geo.to_file(gpkg_filepath, driver="GPKG", layer="polygons")

    # Create a networkx graph (helper)
    G_nx, adj_matrix = create_graph_networkx(geo)
    # Get relevant information of the instance 
    N, V, NB, D = get_instance_information(G_nx, adj_matrix, geo)

    # Create and save the igraph graph
    G_igraph = get_igraph_graph(G_nx, geo)
    graph_filepath = graph_folder_path + f"{ent}.pkl"
    with open(graph_filepath, "wb") as f:
        G_igraph.write_pickle(f)

    # Create a Flow instance for each valid number of regions
    for p in get_p_from_n(N):
        if N>p:
            flow_filepath = flow_folder_path + f"{ent}_{p}.txt"
            Create_Instance_Flow(N, V, NB, D, p, flow_filepath)  


# ----------------------------------------------------------------------
# Create instance of the while country

geo = df.copy()
geo["x"] = geo.centroid.x
geo["y"] = geo.centroid.y
# Save the .gpkg file 
gpkg_filepath = GPKG_folder_path + f"00.gpkg"
geo.to_file(gpkg_filepath, driver="GPKG", layer="polygons")
# Create and save the igraph graph
G_nx, adj_matrix = create_graph_networkx(geo)
G_igraph = get_igraph_graph(G_nx, geo)
graph_filepath = graph_folder_path + f"00.pkl"
with open(graph_filepath, "wb") as f:
    G_igraph.write_pickle(f)


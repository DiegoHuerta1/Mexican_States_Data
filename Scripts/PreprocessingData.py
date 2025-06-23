import pandas as pd
import geopandas as gpd
from utils import columns

# Define the input and output folders
input_folder = "../Data/Raw Data/"
output_folder = "../Data/Processed Data/"

"""_summary_
Preprocessing the Raw Data:

    * INEGI shapefiles for municipalities in Mexico: conjunto_de_datos/00mun.shp
      Obtained from: https://www.inegi.org.mx/temas/mg/default.html#Descargas
    
    * Production data for each municipality in Mexico: CE2019_mun_prod.csv
"""

# Read the shapefile for municipalities
mun = gpd.read_file(input_folder + "conjunto_de_datos/00mun.shp")

# Read and process the production data 
ce2019 = pd.read_csv(input_folder + "CE2019_mun_prod.csv")
ce2019["CVE_ENT"] = ce2019["Entidad"].str[:2]
ce2019["Entidad"] = ce2019["Entidad"].str[3:]
ce2019["CVE_MUN"] = ce2019["Municipio"].str[:3]
ce2019["CVEGEO"] = ce2019["CVE_ENT"] + ce2019["CVE_MUN"] 
ce2019["Municipio"] = ce2019["Municipio"].str[4:]
ce2019["Actividad económica"] = ce2019["Actividad económica"].str[7:]
ce2019["Actividad económica"] = ce2019["Actividad económica"].str.extract(r'^\s*([\d\-]+)')[0].str.strip()
col_index = ["CVEGEO"]
ce2019_pivot = ce2019.pivot(index=col_index, columns="Actividad económica", values='A111A')
ce2019_pivot = ce2019_pivot.div(ce2019_pivot.sum(axis=1), axis=0)
ce2019_pivot = ce2019_pivot.fillna(0)


# Join the production data with the shapefile
mun_ce19 = mun.join(ce2019_pivot, on="CVEGEO", how="inner")
mun_ce19 = mun_ce19.to_crs(6372)

# Save the processed data
mun_ce19.to_file(output_folder+"mun_ce19.gpkg")

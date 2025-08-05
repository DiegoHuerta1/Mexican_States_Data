# Mexican State Data for the p-Regions Problem

This repository contains instances of Mexican state data with INEGI production data, 
designed for the *p-regions* problem.

## Structure

This repository is organized into three main folders:

1. **Data**: Contains raw and processed data for each municipality.
2. **Instances**: Contains instance files for each Mexican state in different formats.
3. **Scripts**: Python scripts for processing data and generating the instances.

---

### 📁 Data

The `Data` folder includes:

- **Raw data**: Shapefiles for Mexican municipalities and production data for each municipality.
- **Processed file**: A `.gpkg` file with polygons and production vectors for each municipality.
  This file is generated using the Python script `PreprocessingData.py`.

---

### 📁 Instances

The `Instances` folder contains subfolders with instances of each state in three formats:

- **Flow Instances**
- **Graph Instances**
- **GPKG Instances**

#### 🔹 Flow Instances

- `.txt` files, each representing an instance for a specific state and number of regions.
- There are 92 files: 32 states × multiple region values.

#### 🔹 GPKG Instances

- `.gpkg` files, one for each of the 32 states plus one for the entire country (33 total).
- Each file contains polygon geometries and production vectors for municipalities.

#### 🔹 Graph Instances

- igraph graphs (`.pkl` files).
- Each file represents a state as a graph:
  - Nodes = municipalities.
  - `"x"` attributes = production vectors.
  - `"name"` attributes = name of each node.
- 33 files in total (32 states + whole country).

---

### 📁 Scripts

The `Scripts` folder contains Python scripts used for data processing and instance generation.

- `PreprocessingData.py`: Generates the preprocessed `.gpkg` file.
- `CreateInstances.py`: Generates all instance files in the `Instances` folder.

---


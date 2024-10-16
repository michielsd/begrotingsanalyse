import os
import csv

import pandas as pd

# Input
GF_MAP = "GF_brondata/clusterdata/"
UF_CSV = "GF_brondata/uitkeringsfactor.csv"
OUTPUT_MAP = "GF_data/"

def main():
    circulaires = get_gf_data(GF_MAP, UF_CSV)
    
    clusters = calculate_clusters(circulaires, UF_CSV)
    
    for key, value in clusters.items():
        print(key)
        value.to_csv(OUTPUT_MAP + key + ".csv")
        


def get_gf_data(gf_map, uf_csv):
    uf_checklist, uf_list = get_uf(uf_csv)
    
    gf_data = []
    
    gf_files = os.listdir(gf_map)
    gewichten_files = [file for file in gf_files if "gewichten" in file.lower()]
    volumina_files = [file for file in gf_files if "volumina" in file.lower()]
    id_gew_files = [file for file in gf_files if "id_gew" in file.lower()]
    siudu_files = [file for file in gf_files if "siudu" in file.lower()]
    
    for g in gewichten_files:
        volumina = any(file.startswith(g[:13]) for file in volumina_files)
        id_gew = any(file.startswith(g[:13]) for file in id_gew_files)
        siudu = any(file.startswith(g[:13]) for file in siudu_files)
        
        if volumina and id_gew and siudu and g[3:13] in uf_checklist:
            gf_data.append(g[:13])
            
    return gf_data


def calculate_clusters(circulaires, uf_csv):
    
    # Define closure to convert values to numeric, with error handling
    def safe_to_numeric(x):
        try:
            return pd.to_numeric(x)
        except ValueError:
            return x
    
    cluster_data_dict = {}
    
    for circulaire in circulaires:
        uf_checklist, uf_list = get_uf(uf_csv)
        
        df_gewichten = pd.read_csv(GF_MAP + circulaire + "_Gewichten.csv") 
        df_volumina = pd.read_csv(GF_MAP + circulaire + "_Volumina.csv")
        df_id_gew = pd.read_csv(GF_MAP + circulaire + "_ID_gew.csv")
        df_siudu = pd.read_csv(GF_MAP + circulaire + "_SIUDU.csv")
        
        # Define indices, set to numeric
        df_gewichten = df_gewichten.set_index("Codering maatstaf")
        df_volumina = df_volumina.set_index("Naam")
        df_id_gew = df_id_gew.set_index("Naam maatstaf")
        df_siudu = df_siudu.set_index("Naam")
        
        df_gewichten = df_gewichten.apply(safe_to_numeric)
        df_volumina = df_volumina.apply(safe_to_numeric)
        df_id_gew = df_id_gew.apply(safe_to_numeric)
        df_siudu = df_siudu.apply(safe_to_numeric)
        
        # Take clusters from gewichten
        clusters = list(df_gewichten.columns[1:])
        
        # Take uitkeringsfactor from circulaire
        uf = float([row for row in uf_list if row.startswith(circulaire[3:])][0][11:])
        
        # Calculate cluster totals per gemeente
        outputdict = {}
        for i, r in df_volumina.iterrows():
            linedict = {}
    
            gemeente = r.name
            volumina_values = r[2:].values
            siudu_values = df_siudu.loc[gemeente].values
            
            for c in clusters:
        
                gewichten_per_cluster = df_gewichten[c].values
                gewichten_siudu = df_id_gew[c].values

                print(gewichten_siudu)
                print(siudu_values)
                if len(volumina_values) == len(gewichten_per_cluster) and len(gewichten_siudu) == len(siudu_values):
                    print("check")
                    cluster_total = uf*sum(v * w for v, w in zip(volumina_values, gewichten_per_cluster))
                    siudu_total = sum()
                    
    
        outputdict[gemeente] = linedict 
        
        cluster_data_dict[circulaire] = pd.DataFrame(outputdict).T
    
    return cluster_data_dict
        

def get_uf(uf_csv):
    with open(uf_csv, mode='r', encoding='utf-8', ) as file:
        csv_reader = csv.reader(file)
        uf_list = list(csv_reader)[1:]
    
    uf_checklist = ["_".join(row[:-1]) for row in uf_list]
    uf_list = ["_".join(row) for row in uf_list]
    
    return uf_checklist, uf_list
        
     
if __name__ == "__main__":
    main()

import os

import pandas as pd

# Globals
IV3_MAP = "Brondata/Iv3/"
CLASSES = "Brondata/Gemeenteklassen/"
ANALYSEMAP = "Analysedata/Iv3/"

def main():
    
    for file in os.listdir(IV3_MAP):
        jaar = file[:4]
        
        # Create output file name
        if file.endswith("000.csv"):
            output_name = f'{jaar}_begroting.csv'
        elif file.endswith("005.csv"):
            output_name =  f'{jaar}_jaarrekening.csv'
    
        # Create output df
        df = pd.read_csv(IV3_MAP + file)
        
        totalen = get_taakveld_totals(df)
        output_df = add_class_data(totalen, jaar)
        
        output_df.to_csv(ANALYSEMAP + output_name)
        print(output_name)
                
def get_taakveld_totals(df):
    g = "Gemeenten"
    t = "TaakveldBalanspost"
    c = "Categorie"
    k = "k_2ePlaatsing_2"

    # Pivot on Gemeenten and TaakveldBalanspost
    pv = df.pivot(index = [g, t], columns=c, values =[k])
    
    # Sum baten and lasten
    pv.columns = [col[-1] for col in pv.columns]
    batencolumns = [col for col in pv.columns if col.startswith("B")]
    lastencolumns = [col for col in pv.columns if col.startswith("L")]

    pv['Baten'] = pv[batencolumns].sum(axis=1)
    pv['Lasten'] = pv[lastencolumns].sum(axis=1)
    
    # Remove Balanspost and columns with Categorie
    pv = pv[pv.index.get_level_values(t).str.startswith(("A", "P")) == False]
    pv = pv.drop(columns=batencolumns + lastencolumns + ['Primo', 'Ultimo'])
  
    df2 = pv.reset_index()
    return df2

def add_class_data(df, jaar):
    
    class_data = pd.read_csv(CLASSES + jaar + ".csv", sep="\t")
    output_df = pd.merge(df, class_data, on="Gemeenten")
    
    return output_df

if __name__ == "__main__":
    main()

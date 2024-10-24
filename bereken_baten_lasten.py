import os

import pandas as pd

# Globals
IV3_MAP = "Brondata/Iv3/"
#GROOTTEKLASSEN PROVINCIES VOOR VERGELIJKING

def main():
    
    for file in os.listdir(IV3_MAP):
        if file.endswith("000.csv"):
            output_name = f'{file[:4]}_begroting'
        elif file.endswith("005.csv"):
            output_name =  f'{file[:4]}_jaarrekening'
    
    
        
        

def pivotIv3(df):
  pv = df.pivot(index = [g, t], columns=c, values =[k])

  pv.columns = [col[-1] for col in pv.columns]
  batencolumns = [col for col in pv.columns if col.startswith("B")]
  lastencolumns = [col for col in pv.columns if col.startswith("L")]

  pv['Baten'] = pv[batencolumns].sum(axis=1)
  pv['Lasten'] = pv[lastencolumns].sum(axis=1)
  pv['Saldo'] = pv.apply(lambda row: row.Baten - row.Lasten, axis=1)

  df2 = pv.reset_index()

  return df2

if __name__ == "__main__":
    main()

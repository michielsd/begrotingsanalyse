import csv
import pandas as pd

# Input
GEWICHTEN = "GF_S22_Gewichten_2023.csv"
VOLUMINA = "GF_S22_Volumina_2023.csv"

# DataFrames based on input
df_gewichten = pd.read_csv(GEWICHTEN, sep=",")
df_volumina = pd.read_csv(VOLUMINA, sep=",")

# DataFrames redux'd for matrix multiplication
# NO CHECKS ON MATRIX SHAPE
df_g = df_gewichten.iloc[:, 2:-1]
df_v = df_volumina.iloc[:, 3:]

gf_aandelen = df_v.dot(df_g)

print(gf_aandelen)

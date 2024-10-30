import csv

import altair as alt
import pandas as pd
import streamlit as st
import matplotlib

# Globals
JAAR_MINIMUM = 2024
JAAR_MAXIMUM = 2024
LAATSTE_JR = 2023
LAATSTE_CRE = "S2024"

# Data import
@st.cache_resource
def get_iv3data(jaar, doc):
    filepath = f"Analysedata/Iv3/{jaar}_{doc}.csv"
    data = pd.read_csv(filepath)

    return data

@st.cache_resource
def get_gfdata(gf_path):
    filepath = f"Analysedata/GF/GF_{gf_path}.csv"
    data = pd.read_csv(filepath)
    
    return data

@st.cache_data
def filter_gfdata(data, gemeente):
    
    # Filter out gemeente
    filtered_data = data[data['Gemeenten'] == gemeente]
    
    return filtered_data

def get_circulaires(jaar):
    circulaire_dict = {}
    
    laatste_jaar = int(LAATSTE_CRE[1:])
    vorig_jaar = int(jaar) - 1
    laatste_maand = "Mei" if LAATSTE_CRE[0] == "M" else "September"
    
    # If no circulaires for jaar: september circulaire last year
    if int(jaar) > laatste_jaar:
        circulaire_dict[f"September {laatste_jaar}"] = f"S{laatste_jaar}_{jaar}"
    # If circulaire in jaar and laatste circulaire is Mei
    elif int(jaar) == laatste_jaar and laatste_maand == "Mei":
        circulaire_dict[f"Mei {jaar}"] = f"M{laatste_jaar}_{jaar}"
        circulaire_dict[f"September {vorig_jaar}"] = f"S{vorig_jaar}_{jaar}"
    elif int(jaar) == laatste_jaar and laatste_maand == "September":
        circulaire_dict[f"September {jaar}"] = f"S{jaar}_{jaar}"
        #circulaire_dict[f"Mei {jaar}"] = f"M{laatste_jaar}_{jaar}"
        #circulaire_dict[f"September {vorig_jaar}"] = f"S{vorig_jaar}_{jaar}"
    
    
    circulaire_list = circulaire_dict.keys()
    
    return circulaire_list, circulaire_dict

@st.cache_data
def filter_iv3data(data, gemeente):
    
    # Filter out gemeente
    filtered_data = data[data['Gemeenten'] == gemeente]
    
    # Calculate saldo
    filtered_data = filtered_data.assign(Saldo=filtered_data['Baten'] - filtered_data['Lasten'])
        
    # Drop superfluous columns
    filtered_data = filtered_data.drop(columns=["Gemeenten", "Provincie", "Gemeentegrootte", "Stedelijkheid", "Inwonertal"])
    filtered_data = filtered_data.set_index("Taakveld")
    
    return filtered_data



############################################################################

############################################################################

# Wide screen
st.set_page_config(layout="wide")

# Body
header_container = st.container()
chart_container = st.container()
iv3_table_container = st.container()

# Sidebar
with st.sidebar:
    st.header("Analyse")
    
    sidebar_jaren = [str(i) for i in range(JAAR_MINIMUM, JAAR_MAXIMUM+1)]
    selected_jaar = st.selectbox("Selecteer het begrotingsjaar",
                                 sidebar_jaren,
                                 index=0,
                                 key=0)
    
    sidebar_gemeenten = get_iv3data(selected_jaar, "begroting").Gemeenten.unique()
    selected_gemeente = st.selectbox("Selecteer de gemeente",
                                 sidebar_gemeenten,
                                 key=1)
    
    
    overhead_select = st.toggle("Overhead toegedeeld?")


with header_container:
    h1, h2, h3 = st.columns([2, 4, 2])

    with h2:
        st.title("📊 Begrotingsanalyse")
        st.markdown(
            "Begrotingsanalyse"
        )
        st.markdown(
            "Dit is een voorlopige versie, fouten voorbehouden. Vragen of opmerkingen? Stuur een mail naar <postbusiv3@minbzk.nl>."
        )


with chart_container:
    h1, h2, h3 = st.columns([2, 4, 2])
    
    with h2:
        circulaires, circulaire_dict = get_circulaires(selected_jaar)
        selected_circulaire = st.selectbox("Selecteer de circulaire",
                                 circulaires,
                                 index=0,
                                 key=3)
    
        gf_cluster_data = filter_gfdata(get_gfdata(circulaire_dict[selected_circulaire]), selected_gemeente)
        st.write(gf_cluster_data)


with iv3_table_container:
    h1, h2, h3 = st.columns([2, 4, 2])
    
    with h2:
        documenten = ["Begroting", "Jaarrekening"] if int(selected_jaar) <= LAATSTE_JR else ["Begroting"]
        selected_doc = st.selectbox("Begroting- of jaarrekeningdata?",
                                 documenten,
                                 key=2)
        with st.form("data_editor_form"):
            submit_button = st.form_submit_button("Update de grafiek")
            gemeente_iv3data = filter_iv3data(get_iv3data(selected_jaar, selected_doc), selected_gemeente)
            
            st.data_editor(gemeente_iv3data,  use_container_width=True,)
            
            if submit_button:
                pass
    
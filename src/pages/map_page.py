import streamlit as st
import pandas as pd
import altair as alt

# --- Nouvelle fonction pour charger les données ---
@st.cache_data # Utilise le cache de Streamlit
def load_data(file_path):
    df = pd.read_csv(file_path) 
    return df
# --------------------------------------------------

# --- Nouvelle fonction pour créer la carte ---
def create_prefecture_map(df):
    url_geojson = 'https://static.data.gouv.fr/resources/contours-des-communes-de-france-simplifie-avec-regions-et-departement-doutre-mer-rapproches/20210210-183703/a-dep2020-geojson.json'
    data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='features',type='json'))

    maps = alt.Chart(data_geojson_remote).mark_geoshape().transform_lookup(
                lookup='properties.dep',
                from_=alt.LookupData(df, 'code', ['code', 'Préfecture', 'Note sur 5', 'Total des avis'])
            ).encode(
                color=alt.Color("Note sur 5:Q"),
                tooltip=["Préfecture:N", 'code:N', "Note sur 5:Q", 'Total des avis:N']
            ).project(
                type='identity', reflectY=True
            )
    return maps
# ----------------------------------------------

def main():
    st.title("Carte des notes moyennes des préfectures en France et DOM-TOM")
    st.write("Source des données : Google Maps")

    # Appel de la fonction pour charger les données
    df = load_data("data/my_data.csv")

    # Appel de la fonction pour créer la carte
    map_chart = create_prefecture_map(df)
    st.altair_chart(map_chart, use_container_width=True)

if __name__ == '__main__':
    main()
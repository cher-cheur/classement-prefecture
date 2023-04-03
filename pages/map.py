#myenv\Scripts\activate
#streamlit run str.py

import streamlit as st
import pandas as pd
import altair as alt

def main():
    st.title("Carte des notes moyennes des préfectures en France et DOM-TOM")
    st.write("Source des données : Google Maps")

    df = pd.read_excel("my_data_code.xlsx")

    url_geojson = 'https://static.data.gouv.fr/resources/contours-des-communes-de-france-simplifie-avec-regions-et-departement-doutre-mer-rapproches/20210210-183703/a-dep2020-geojson.json'
    data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='features',type='json'))

    maps= alt.Chart(data_geojson_remote).mark_geoshape().transform_lookup(
                lookup = 'properties.dep',
                from_ = alt.LookupData(df, 'code', ['code','Préfecture','Note sur 5','Total des avis'])
            ).encode(
            #tooltip = 'properties.NAME_2:N',
                color=alt.Color("Note sur 5:Q"),
                tooltip = ["Préfecture:N",'code:N',"Note sur 5:Q",'Total des avis:N']
            ).project(
                type='identity', reflectY=True
            )

    st.altair_chart(maps, use_container_width=True)

if __name__ == '__main__':
    main()



#myenv\Scripts\activate
#streamlit run str.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import altair as alt

def main():
    st.title("Rapport général sur les préfectures en France")
    st.write("Source des données : Google Maps")

    # Read CSV file
    #df = pd.read_csv("my_data_test.csv", delimiter = ';',encoding='ISO-8859-1')
    df = pd.read_excel("my_data_code.xlsx")

    df = df.sort_values(by='Note sur 5', ascending=False)

    moyenne = df['Note sur 5'].mean()
    total = sum(df['Total des avis'])
    q9 = df['Note sur 5'].quantile(0.90)

    st.markdown("## 🏥 Santé des préfectures en France")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre total des avis", total)
    col2.metric("Note moyenne des préféctures", round(moyenne, 2))
    col3.metric("90\% ont une note inférieure à ", round(q9, 2))

    #Top 10
    df_10 = df.head(10)

    st.markdown("## Meilleurs 10 préfectures en France")

    bars = alt.Chart(df_10).mark_bar(
        cornerRadius= 50).encode(
            x=alt.X('Note sur 5', axis=None),
            y=alt.Y('Préfecture', sort='-x'),
            color = alt.Color("Note sur 5", legend = None),
            tooltip = ["Préfecture","code", "Note sur 5", "Total des avis"],
            text = 'Note sur 5'
        )

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3,  # Nudges text to right so it doesn't appear on top of the bar
        )

    chart = (bars + text).properties(height = 600)

    st.altair_chart(chart, use_container_width=True)
 

if __name__ == '__main__':
    main()

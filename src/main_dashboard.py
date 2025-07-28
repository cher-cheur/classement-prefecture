#myenv\Scripts\activate
#streamlit run str.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import altair as alt

# --- Nouvelle fonction pour charger les données ---
@st.cache_data # Utilise le cache de Streamlit pour éviter de recharger les données à chaque interaction
def load_data(file_path):
    df = pd.read_csv(file_path)
    df = df.sort_values(by='Note sur 5', ascending=False)
    return df

# --- Nouvelle fonction pour afficher les métriques générales ---
def display_general_report(df):
    moyenne = df['Note sur 5'].mean()
    total = sum(df['Total des avis'])
    q9 = df['Note sur 5'].quantile(0.90)

    st.markdown("## 🏥 Santé des préfectures en France")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre total des avis", total)
    col2.metric("Note moyenne des préfectures", round(moyenne, 2))
    col3.metric("90\% ont une note inférieure à ", round(q9, 2))

# --- Nouvelle fonction pour afficher le Top 10 ---
def display_top_10_chart(df):
    df_10 = df.head(10)
    st.markdown("## Meilleurs 10 préfectures en France")

    bars = alt.Chart(df_10).mark_bar(
        cornerRadius=50).encode(
            x=alt.X('Note sur 5', axis=None),
            y=alt.Y('Préfecture', sort='-x'),
            color=alt.Color("Note sur 5", legend=None),
            tooltip=["Préfecture", "code", "Note sur 5", "Total des avis"],
            text='Note sur 5'
        )

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3,
    )

    chart = (bars + text).properties(height=600)
    st.altair_chart(chart, use_container_width=True)

def main():
    st.title("Rapport général sur les préfectures en France")
    st.write("Source des données : Google Maps")

    df = load_data("data/my_data.csv")

    display_general_report(df)

    # Appel de la nouvelle fonction pour afficher le Top 10
    display_top_10_chart(df)

if __name__ == '__main__':
    main()

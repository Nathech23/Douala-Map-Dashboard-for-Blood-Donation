import folium
import folium.features
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import json

APP_TITLE = "🩸📊 BLOOD CAMPAIGN"

def display_map(file):
    # Charger le CSV contenant les occurrences par quartier
    df = pd.read_csv(file, sep=";", encoding="utf-8-sig")
    
    # Charger manuellement le GeoJSON avec le bon encodage
    with open('quartiers_douala.geojson', encoding='utf-8-sig') as f: 
        geojson_data = json.load(f)
    
    # Pour chaque feature du GeoJSON, ajouter le nombre d'occurrences provenant du CSV
    # On suppose que le nom dans le CSV est en minuscules (voir le traitement dans main_data)
    for feature in geojson_data["features"]:
        quartier_geo = feature["properties"]["nom"].strip().lower()
        # Chercher la ligne correspondante dans le DataFrame
        ligne = df[df["Quartier"] == quartier_geo]
        if not ligne.empty:
            occurrence = int(ligne.iloc[0]["Occurrences"])
        else:
            occurrence = 0
        feature["properties"]["occurrences"] = occurrence

    # Créer la carte centrée sur Douala
    m = folium.Map(location=[4.05, 9.75], zoom_start=12.5, scrollWheelZoom=False, tiles='CartoDB positron')
    
    # Créer le choropleth avec coloration basée sur 'Occurrences'
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        data=df,
        columns=("Quartier", "Occurrences"),
        key_on="feature.properties.nom",
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.8,
        legend_name="Nombre d'occurrences de donneurs",
        highlight=True
    )
    choropleth.geojson.add_to(m)
    
    # Ajouter un tooltip indiquant le nom du quartier et le nombre d'occurrences
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=["nom", "occurrences"],
            aliases=["Quartier: ", "Occurrences: "],
            localize=True
        )
    )
    
    st_map = st_folium(m, width=700, height=450)

def load_data(file):
    df = pd.read_csv(file, sep=";")
    #don = "Oui"
    #df = df[df['A-t-il (elle) déjà donné le sang'] == don]  # Filtrer les donneurs
    #df.to_csv("donneurs_oui.csv", sep=";", index=False, encoding="utf-8-sig")
    #df = pd.read_csv("donneurs_oui.csv", sep=';', encoding='utf-8-sig')  #Regroupement des donneurs par quartier
    #df_trie = df.sort_values(by='Quartier de Résidence')
    #df_trie.to_csv('donnees_tries.csv', index=False, sep=';', encoding='utf-8-sig')
    
    st.header("Liste des donneurs")
    st.write(df.shape)
    st.write(df.head())
    st.write(df.columns)

def main_data():
    # Lire le fichier CSV initial
    #df = pd.read_csv(file, sep=";", encoding='utf-8')

    # Normaliser les noms de quartiers (insensibles à la casse)
    #df['Quartier de Résidence'] = df['Quartier de Résidence'].str.strip().str.lower()

    # Compter le nombre d'occurrences par quartier
    #quartier_counts = df['Quartier de Résidence'].value_counts().reset_index()

    # Renommer les colonnes
    #quartier_counts.columns = ['Quartier', 'Occurrences']

    # Enregistrer le résultat
    #quartier_counts.to_csv("quartiers_occurrences.csv", index=False, sep=';', encoding='utf-8-sig')

    df = pd.read_csv("quartiers_occurrences.csv", sep=";", encoding='utf-8')    
    st.header("Liste des quartiers où il y a des donneurs")
    st.write(df.shape)
    st.write(df.head())
    st.write(df.columns)
    
def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)

    # Charger et préparer les données
    load_data("donneurs_oui.csv")
    main_data()#'donnees_tries.csv'

    # Afficher la carte
    display_map("quartiers_occurrences.csv")
    
if __name__ == "__main__":
    main()

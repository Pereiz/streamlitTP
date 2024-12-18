# -- coding: utf-8 --
"""
Created on Wed Dec 04 10:45:10 2024

@author: Guillermo
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.header(':blue[Traitement de données]')

# Chargement du fichier CSV
file = st.file_uploader("Importer vos données ici", type=["csv"])

# Si un fichier est téléchargé
if file is not None:
    data = pd.read_csv(file)

    # Affichage du fichier chargé
    st.write(f"Vous avez téléchargé un fichier contenant {data.shape[0]} lignes et {data.shape[1]} colonnes.")
    
    # Création des colonnes pour l'affichage et le téléchargement
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Base de données")
    with col2:
        if st.button("Télécharger"):
            st.markdown('<p style="color: green;">Vous venez de télécharger la base!</p>', unsafe_allow_html=True)

    # Affichage des données avec un expander
    with st.expander("Cliquez pour afficher le contenu de la base de données", False):
        st.write(data)

    # Renommer les colonnes pour avoir A, B, C, ...
    try:
        column_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        data.columns = column_names[:data.shape[1]]  # Ajuste en fonction du nombre de colonnes
        data_numeric = data[["A", "B", "I"]].apply(pd.to_numeric, errors='coerce')  # Sélectionne "A", "B" et "I"

        # Vérifie si les colonnes sélectionnées contiennent des valeurs numériques
        if not data_numeric.empty:
            st.write("Colonnes utilisées pour les graphiques :")
            st.write(data_numeric.columns.tolist())

            # Choix du type de graphique
            chart_type = st.selectbox("Choisissez le type de graphique", ["Ligne", "Bâton", "Nuage de points"])

            # Graphique en ligne
            if chart_type == "Ligne":
                st.success("Graphique en ligne (colonnes A, B, I)")
                st.line_chart(data_numeric)
            
            # Graphique en bâton
            elif chart_type == "Bâton":
                st.warning("Graphique en bâton (colonnes A, B, I)")
                st.bar_chart(data_numeric)
            
            # Graphique en nuage de points
            elif chart_type == "Nuage de points":
                st.info("Graphique en nuage de points (colonnes A, B, I)")
                st.pyplot(data_numeric.plot(kind='scatter', x='A', y='B').get_figure())
        
        else:
            st.warning("Aucune donnée valide trouvée dans les colonnes sélectionnées (A, B, I).")

    except KeyError as e:
        st.error(f"Erreur : certaines colonnes spécifiées sont absentes du fichier. Détail : {e}")
        
    # Options de normalisation des données
    normalize = st.checkbox("Normaliser les données", value=False)
    if normalize:
        data_numeric = (data_numeric - data_numeric.min()) / (data_numeric.max() - data_numeric.min())
        st.write("Les données ont été normalisées.")

    # Graphique avec matplotlib
    st.subheader("Histogramme de la base de données")
    x = np.linspace(-1 * np.pi, 1.5 * np.pi, 100)
    y = np.sin(x)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    st.pyplot(fig)

    # Graphique en ligne avec des colonnes aléatoires
    st.subheader("Ligne graphique de la base de données")
    df = data_numeric  # Utiliser les colonnes A, B et I de data_numeric
    st.line_chart(df)

else:
    st.warning("Veuillez télécharger un fichier CSV pour commencer. Exemple : IRIS.CSV")


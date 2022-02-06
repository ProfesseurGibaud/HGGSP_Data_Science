# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 10:17:36 2022

@author: Sylgi
"""

import pandas as pd
from pre_training import *


df = pd.read_csv("data_questionnaires.csv",sep = ";")
df = df.drop(columns = ["ID de la réponse","Date de soumission","Dernière page", "Langue de départ","Tête de série", "Date de lancement", "Date de la dernière action"])
names_columns = df.columns

def choix_colonnes(df,debut,fin):
    # 35 - > 39 : Première aisé
    # 40 -> 45 : Terminale aisé
    small_df = df[names_columns[debut:fin+1]]
    #small_df = small_df.dropna()
    return small_df

def count(df):
    dico_count = {}
    liste_mauvais_index = []
    for index,row in df.iterrows():
        print(index, list(row))
        try:
            if " ".join(list(row)) not in dico_count:
                dico_count[" ".join(list(row))] = 1
            else:
                dico_count[" ".join(list(row))] += 1
        except:
            liste_mauvais_index.append(index)
    return dico_count,liste_mauvais_index

def make_dico(df,debut,fin):
    small_df = choix_colonnes(df, debut, fin)
    dico_count,liste = count(small_df)
    return dico_count,liste
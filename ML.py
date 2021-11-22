# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:52:28 2021

@author: Sylvain
"""

import openpyxl
from copy import deepcopy
import pandas as pd
from Nettoyage import *
import numpy as np
from Fonctions_analyse import *
import sqlite3
from collections import Counter

df = pd.read_csv("data_questionnaires.csv",sep = ";")
df = df.drop(columns = ["ID de la réponse","Date de soumission","Dernière page", "Langue de départ",
         "Tête de série", "Date de lancement", "Date de la dernière action" ])



list_column_numeros_exploser = [0,2,3,21,24,34]
list_numeros_supprimer  = []


def explode_list_columns(list_column_numeros,data_frame = df):
    columns_names = df.columns
    list_column_names = []
    for num in list_column_numeros:
        list_column_names.append(columns_names[num])
    for nom_colonne in list_column_names:
        data_frame = explode_one_column(nom_colonne)
    return data_frame

def explode_one_column(nom_colonne,data_frame = df):
    colonne = data_frame.pop(nom_colonne)
    names_columns = set(colonne.values)
    for name in names_columns:
        new_column =  [1*(name == data) + 0*(name != data) for data in colonne]
        data_frame.loc[:,name] = new_column
    return data_frame


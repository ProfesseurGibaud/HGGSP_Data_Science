# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:52:28 2021

@author: Sylvain
"""


from copy import deepcopy
import pandas as pd
from Nettoyage import *
import numpy as np
from numpy import nan
from Fonctions_analyse import *
import sqlite3
from collections import Counter

df = pd.read_csv("data_questionnaires.csv",sep = ";")
df = df.drop(columns = ["ID de la réponse","Date de soumission","Dernière page", "Langue de départ",
         "Tête de série", "Date de lancement", "Date de la dernière action" ])

nom_colonne = df.columns
list_suppr = [2,4,20,22,25,27,28,
              29,67,68,69,70,72,73,
              75,81,93,103,58,60,62,64,66]



def suppr_columns(list_column_numeros,df):
    columns_names = df.columns
    list_column_names = []
    for num in list_column_numeros:
        list_column_names.append(columns_names[num])
        print(columns_names[num])
    df = df.drop(columns = list_column_names)
    return df

df = suppr_columns(list_suppr, df)





def nettoyage_age(df): # A lancer manuellement ! 
    nom_colonne_age = df.columns[1]
    colonne_age = df[nom_colonne_age]
    nvx_colonne_age = []
    for age in colonne_age:
        if type(age) != float:
            try:
                print(int(age))
                nvx_colonne_age.append(int(age))
            except:
                print("Erreur")
                nvx_colonne_age.append(None)
        else:
            nvx_colonne_age.append(None)
    df[nom_colonne_age] = nvx_colonne_age
    
def nettoyage_concours(df): # A lancer manuellement ! 
    nom_colonne_concours = df.columns[3]
    print(nom_colonne_concours)
    colonne_concours = df[nom_colonne_concours]
    nvx_colonne_concours = []
    for concours in colonne_concours:
        if type(concours) != float:
            try:
                print(int(concours))
                nvx_colonne_concours.append(int(concours))
            except:
                print("Erreur")
                nvx_colonne_concours.append(None)
        else:
            nvx_colonne_concours.append(None)
    df[nom_colonne_concours] = nvx_colonne_concours

def Sex(df):
    dico = {"Un homme" : -1, "Une femme" : 1}
    nom_colonne = df.columns[0]
    print(nom_colonne)
    df[nom_colonne].replace(dico,inplace=True)


def Statut(df):
    dico = {"Certifié.e": 1, "Agrégé.e externe en géographie":3, "Agrégé.e interne":2, "Certifié.e interne": 0.5,"Agrégé.e externe en histoire":2.5,"Autre":0}
    nom_colonne = df.columns[2]
    print(nom_colonne)
    df[nom_colonne].replace(dico,inplace=True)

def Parcours(df):
    Prépa_Oui_Non = {}
    Géographie_Oui_Non = {}
    Doctorat_Oui_Non = {}
    Fac_IEP_ENS = {0,1,2}


def FormeGeopo(df):
    dico = {"Formation Initiale":4, "Formation Continue":3, "Auto-Formation":2, "Pas assez": 0}

def Theme(df):
    pass

          
#df = df.fillna(inplace=True)

df = df.dropna()    


from sklearn import linear_model
name_colonnes = df.columns
numero = 48
def separation_df_train_target(numero_colonne,df):
    name_column_target = df.columns[numero]
    target = df.pop(name_column_target)
    return df, target

def Lasso(alpha ,target,df):
    clf = linear_model.Lasso(alpha=0.1)
    clf.fit(df,target)
    return clf.coef_
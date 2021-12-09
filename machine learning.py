# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:52:28 2021

@author: Sylvain
"""


import pandas as pd
from pre_training import *

df = pd.read_csv("data_questionnaires.csv",sep = ";")





df = df.drop(columns = ["ID de la réponse","Date de soumission","Dernière page", "Langue de départ","Tête de série", "Date de lancement", "Date de la dernière action"])

df = suppr_columns(df)
replace_classe(df)
df = replace_parcours(df)
nettoyage_age(df)
nettoyage_concours(df)
replace_gender(df)
replace_statut(df)
replace_lycee(df)
replace_choix_ensgn(df)
replace_volonte_formation(df)
replace_pourcentage(df)
df = replace_type_formation(df)
df = replace_theme_prof(df)
df.drop("Votre établissement propose la spécialité histoire-géographie, géopolitique, sciences politiques :",axis = 1,inplace = True)
df = replace_methodo(df)
replace_oui_non(df)
df = replace_theme_eleve(df)
df = df.dropna()    

from sklearn import linear_model
name_colonnes = df.columns
numero = 20


def separation_df_train_target(numero_colonne,df):
    dff = deepcopy(df)
    name_column_target = df.columns[numero_colonne]
    target = dff.pop(name_column_target)
    return dff, target

def make_Lasso(alpha ,target,dff):
    clf = linear_model.Lasso(alpha=alpha)
    name_columns = dff.columns
    clf.fit(dff,target)
    result = pd.DataFrame({"Nom Variable" : name_columns,"Coefficients":list(clf.coef_)})
    return result

def Lasso(numero,df,alpha = 0.1):
    dff,target = separation_df_train_target(numero, df)
    result = make_Lasso(alpha, target, dff)
    return result
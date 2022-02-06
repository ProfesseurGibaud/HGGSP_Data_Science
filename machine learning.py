# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:52:28 2021

@author: Sylvain
"""



"""

Utilisation du programme : 
    1°) Lancer le script complet 
    2°) Dans l'explorateur de variable, double cliquer sur name_colonnes
    3°) Noter les numéros des colonnes que vous cherchez à expliquer 
    (les colonnes des phénomènes qui vous interessent)
    4°) Dans la console (en bas à droite) écrivez : 
        result = Lasso(le numero de la colonne,df)
    
        Exemple : si je veux ce qui détermine (statistiquement) si un professeur 
        établit une distinction claire entre géopolitique et relations internationales.
        Je vois que cette question est traitée dans la colonne 9 et j'écris alors :
            result = Lasso(9,df)
    5°) Les nombres positifs signifie que les variables augmentent en même temps,
        Les nombres négatifs signifie que si une variable augmente l'autre diminue
    6°) Dans le cas où les résultats ne sont pas satisfaisant (trop de zéros ou pas assez)
    il est possible d'ajuster le degré de selection en écrivant par exemple à la place :
        result = Lasso(9,df,alpha = 0.001)
    plus le alpha sera petit moins on aura de 0, plus il sera grand, plus on aura de 0.
    Initialement alpha est de 0.1

    7°) La spécialiste de la question (ou doctorante) cherche quelles sont les raisons 
    pour lesquelles on observe ses corrélations.
    En ajoutant des questions sur ces questionnaires, faisant des conjectures etc ... 
    
    :D
    
    
    
    Sylvain out !!! (et heureux)
"""










import pandas as pd
from pre_training import *


df = pd.read_csv("data_questionnaires.csv",sep = ";")
df = df.drop(columns = ["ID de la réponse","Date de soumission","Dernière page", "Langue de départ","Tête de série", "Date de lancement", "Date de la dernière action"])

def data_cleansing(df):
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
    #df = renormalisation(df)
    return df


df = data_cleansing(df)

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
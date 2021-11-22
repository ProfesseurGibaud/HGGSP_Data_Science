

# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 14:29:11 2021

@author: Sylgi






"""

import openpyxl
import pandas as pd
from Nettoyage import *
import numpy as np
from Fonctions_analyse import *
import sqlite3
from collections import Counter


conn = sqlite3.connect("RéponseQuestionnaires.db")
cursor = conn.cursor()


response_workbook = openpyxl.load_workbook(r"reponses.xlsx")
response_sheet = response_workbook.active
#print(response_sheet.cell(row = 1,column = 1).value)

indication_workbook = openpyxl.load_workbook(r"indications.xlsx")
indication_sheet = indication_workbook.active
#print(indication_sheet.cell(row = 1,column = 1).value)


#Liste Age et Annee

liste_age = [item.value for item in response_sheet["I"]]
liste_age = liste_age[1:]
liste_age = nettoyage_age(liste_age)



liste_annee_concours = [item.value for item in response_sheet["M"]]
liste_annee_concours = nettoyer_concours(liste_annee_concours)



# Liste Parcours

liste_ordonnee_parcours,nbre_parcours = de_sql_vers_liste_pourcentage("parcours_académique", cursor)


# Liste Enseignement

liste_enseignement,nbre_enseignement = de_coord_vers_liste_pourcentage("AF", response_sheet,"Enseignement")

#Si il y a une formation : précise les contenus "AH"


liste_formation_oui_non,nbre_formation = de_coord_vers_liste_pourcentage("AH", response_sheet,"Contenus Formation")


#A l'aise


liste_ordonne_theme_aise,nombre_aise = de_sql_vers_liste_pourcentage("a_l_aise", cursor)


# pas à l'aise

liste_ordonne_theme_pas_aise,nombre_pas_aise = de_sql_vers_liste_pourcentage("moins_a_l_aise", cursor)


# Définition géopolitique

string = de_coord_vers_txt("Geopolitique","CC", response_sheet)

# Formation type contenu

string = de_coord_vers_txt("Formation_type_contenu", "AJ", response_sheet)

# Ce que vous voulez de la formation

string = de_coord_vers_txt("Ce_que_vous_voulez_de_la_formation", "AK", response_sheet)

# Se considère comme formé 

liste_ordonne_considere_formee,n_formee = de_sql_vers_liste_pourcentage("considere_forme", cursor,split_boolean = False)

# Premiere, Terminale, les deux

liste_classe,n_classe = de_coord_vers_liste_pourcentage("AP", response_sheet,"Classe")

# Méthodologie 

liste_methodo,n_methodo = de_sql_vers_liste_pourcentage("méthodologies", cursor, split_boolean = False)

#Coté positif

string = de_coord_vers_txt("Cotés positifs","BY",response_sheet)

#Coté négatif

string = de_coord_vers_txt("Cotés négatifs","BZ",response_sheet)

#Influence sur histoire géo

liste_influence,n_influence = de_coord_vers_liste_pourcentage("CA",response_sheet,"Influence sur histoire-geo")

#Influence comment 
string = de_coord_vers_txt("Influence Comment", "CB", response_sheet)


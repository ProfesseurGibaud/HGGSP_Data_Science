

# -*- coding: utf-8 -*-
"""

Descriptif du programme :

Dans la suite du programme il y a des #, chaque # correspond à une nouvelle question.

Avant le = il y a un ou deux termes séparés par une virgule par exemple : 
    liste_ordonnee_parcours , nbre_parcours 
liste_ordonnee_parcours est la liste des résultats en pourcentage
n_parcours est le nombre de réponses totales

Tu trouves toutes les réponses (avec leur noms correspondants dans la fenêtre en haut à droite dans l'onglet variable explorer)
                    
                                
Dernière chose dans certaines fonctions il y a :
    split_boolean=True
Cela veut dire que l'algorithmesépare les multiples réponses d'une personne, par exemple si quelqu'un dis qu'il aime les thème 1,2,3 cela va ajouter augmenter les pourcentage de 1,2 et 3 mais cela ne va pas faire une catégorie 1,2,3.
Si tu veux avoir les pourcentages avec les catégories 1,2,3 tu remplaces :
    split_boolean=True par split_boolean=False
    

Tu me disais qu'il fallait que je te forme à l'informatique. C'est exactement le genre de travail que l'on peut donner à des secondes en SNT :D


Je t'aime (amuse toi bien)


PS : Liste Age et Concours sont différents (normalement tu as les bons histogrammes sur ton ordi)


"""

import openpyxl
#import pandas as pd
from Nettoyage import *
import numpy as np
from Fonctions_analyse import *
import sqlite3
from collections import Counter


conn = sqlite3.connect("RéponseQuestionnaires.db")
cursor = conn.cursor()


response_workbook = openpyxl.load_workbook(r"reponses.xlsx")
response_sheet = response_workbook.active


indication_workbook = openpyxl.load_workbook(r"indications.xlsx")
indication_sheet = indication_workbook.active






# Question 6 : Renseignez votre parcours Académique

liste_ordonnee_parcours,nbre_parcours = de_sql_vers_liste_pourcentage("parcours_académique", cursor,split_boolean=True)


# Question 10 : Vous enseignez la géopolitique (oui par choix , etc ...)

liste_enseignement,nbre_enseignement = de_coord_vers_liste_pourcentage("AF", response_sheet,"Enseignement")

#Question 11 : Avez vous reçu une formation à l'enseignement de spécialité ? (Pour moi le reste, Si il y a une formation : précise les contenus "AH"


liste_formation_oui_non,nbre_formation = de_coord_vers_liste_pourcentage("AH", response_sheet,"Contenus Formation")


#Thème où le professeur se sent à l'aise 


liste_ordonne_theme_aise,nombre_aise = de_sql_vers_liste_pourcentage("a_l_aise", cursor,split_boolean=True)


# Thème où le professeur ne se sent pas à l'aise

liste_ordonne_theme_pas_aise,nombre_pas_aise = de_sql_vers_liste_pourcentage("moins_a_l_aise", cursor,split_boolean = True)


# Définition géopolitique (tu peux regarder les nuages de mots)

string = de_coord_vers_txt("Geopolitique","CC", response_sheet)

# Formation type contenu (tu peux regarder les nuages de mots)

string = de_coord_vers_txt("Formation_type_contenu", "AJ", response_sheet)

# Ce que vous voulez de la formation (tu peux regarder les nuages de mots)

string = de_coord_vers_txt("Ce_que_vous_voulez_de_la_formation", "AK", response_sheet)

# Question 14 : Vous considérez vous comme formé à la géopolitique et à son enseignement

liste_ordonne_considere_formee,n_formee = de_sql_vers_liste_pourcentage("considere_forme", cursor,split_boolean = False)

# Question 15 : Vous enseignez l'HGGSP en Premiere, Terminale, les deux

liste_classe,n_classe = de_coord_vers_liste_pourcentage("AP", response_sheet,"Classe")

# Question 18 : Quelle méthodologie mettez vous en place ?

liste_methodo,n_methodo = de_sql_vers_liste_pourcentage("méthodologies", cursor, split_boolean = False)

#Coté positif (tu peux regarder les nuages de mots)

string = de_coord_vers_txt("Cotés positifs","BY",response_sheet)

#Coté négatif(tu peux regarder les nuages de mots)

string = de_coord_vers_txt("Cotés négatifs","BZ",response_sheet)

#Question 21 : L'ensignement de Spécialité influe-t-il sur le tronc commun ? 

liste_influence,n_influence = de_coord_vers_liste_pourcentage("CA",response_sheet,"Influence sur histoire-geo")

#Influence comment (tu peux regarder les nuages de mots)
string = de_coord_vers_txt("Influence Comment", "CB", response_sheet)

#Liste Age et Annee

liste_age = [item.value for item in response_sheet["I"]]
liste_age = liste_age[1:]
liste_age = nettoyage_age(liste_age)



liste_annee_concours = [item.value for item in response_sheet["M"]]
liste_annee_concours = nettoyer_concours(liste_annee_concours)

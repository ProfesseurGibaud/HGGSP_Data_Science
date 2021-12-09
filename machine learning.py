# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:52:28 2021

@author: Sylvain
"""


from copy import deepcopy
import pandas as pd


df = pd.read_csv("data_questionnaires.csv",sep = ";")



df = df.drop(columns = ["ID de la réponse","Date de soumission","Dernière page", "Langue de départ",
         "Tête de série", "Date de lancement", "Date de la dernière action"])


def suppr_columns(df):
    nom_colonne = df.columns
    list_suppr = [2,4,20,22,25,27,28,
              29,67,68,69,70,72,73,
              75,81,93,103,58,60,62,64,66]
    columns_names = df.columns
    list_column_names = []
    for num in list_suppr:
        list_column_names.append(columns_names[num])
        #print(columns_names[num])
    df = df.drop(columns = list_column_names)
    return df

def nettoyage_age(df): 
    nom_colonne_age = df.columns[1]
    colonne_age = df[nom_colonne_age]
    colonne_age.fillna(0)
    nvx_colonne_age = []
    for age in colonne_age:
        if type(age) != float:
            try:
                #print(int(age))
                nvx_colonne_age.append(int(age))
            except:
                #print("Erreur")
                nvx_colonne_age.append(None)
        else:
            nvx_colonne_age.append(None)
    nvx_colonne_age = pd.Series(nvx_colonne_age)
    nvx_colonne_age = nvx_colonne_age - min(nvx_colonne_age)
    #on va renormaliser l'age
    
    df[nom_colonne_age] = nvx_colonne_age
    
def nettoyage_concours(df): # A lancer manuellement ! 
    nom_colonne_concours = df.columns[3]
    print(nom_colonne_concours)
    colonne_concours = df[nom_colonne_concours]
    colonne_concours.fillna(0)
    nvx_colonne_concours = []
    for concours in colonne_concours:
        if type(concours) != float:
            try:
                #print(int(concours))
                nvx_colonne_concours.append(int(concours))
            except:
                #print("Erreur")
                nvx_colonne_concours.append(None)
        else:
            nvx_colonne_concours.append(None)
    nvx_colonne_concours = pd.Series(nvx_colonne_concours)
    nvx_colonne_concours = nvx_colonne_concours - min(nvx_colonne_concours)
    df[nom_colonne_concours] = nvx_colonne_concours

def replace_gender(df):
    dico = {"Un homme" : -1, 
            "Une femme" : 1,
            "Je ne souhaite pas partager cette information":0,
            "Autre":0}
    nom_colonne = df.columns[0]
    #print(nom_colonne)
    df[nom_colonne].replace(dico,inplace=True)


def replace_statut(df):
    dico = {"Certifié.e": 1, 
            "Agrégé.e externe en géographie":3, 
            "Agrégé.e interne":2,
            "Certifié.e interne": 0.5,
            "Agrégé.e externe en histoire":2.5,
            "Contractuel.le":0,
            "Autre":0}
    nom_colonne = df.columns[2]
    #print(nom_colonne)
    df[nom_colonne].replace(dico,inplace=True)

def make_parcours(df):
    name_colonnes = df.columns
    liste_name_columns = name_colonnes[4:18]
    extract = df[liste_name_columns]
    extract.replace({"Oui":1,"Non":0},inplace = True)
    """
    0 : AL
    1 : BL
    2 : ECS
    3 : Fac Geo Licence
    4 : Fac Geo Master 
    5 : Fac Histoire Licence
    6 : Fac Histoire Master
    7 : Autre discipline Licence
    8 : Autre Discipline Master
    9 : ENS
    10 : IEP
    11 : Doctorat Histoire
    12 : Doctorat Géographie  
    13 : Doctorat autre
    """
    def prepa(extract,valeur):
        extract_prepa = extract[extract.columns[0:2+1]]
        column_prepa = valeur * extract_prepa.max(axis = 1)
        column_prepa.name = "Prépa Oui ou Non"       
        return column_prepa
    def licence(extract,valeur):
        extract_licence = extract.iloc[:,[3,5,7]]
        column_licence = valeur* extract_licence.max(axis = 1)
        column_licence.name = "Licence Oui ou Non"
        return column_licence
    def Master(extract,valeur):
        extract_master = extract.iloc[:,[4,6,8]]
        column_master = valeur*extract_master.max(axis = 1)
        column_master.name = "Master Oui ou Non"
        return column_master
    def IEP_ENS(extract,valeur):
        extract_iens = extract.iloc[:,[9,10]]
        column_iens = valeur*extract_iens.max(axis = 1)
        column_iens.name = "IEP,ENS oui ou non"
        return column_iens
    def doctorat(extract,valeur):
        extract_doct = extract.iloc[:,[11,13]]
        column_doct = valeur*extract_doct.max(axis = 1)
        column_doct.name = "Doctorat oui ou non"
        return column_doct
    
    
    parcours = pd.concat([licence(extract,3),Master(extract, 5), IEP_ENS(extract, 6),doctorat(extract, 8)],axis = 1).max(axis = 1)
    parcours += prepa(extract, 0.5)
    parcours.name = "Parcours"
    #On va choisir arbitrairement de compter le nombre d'années d'étude et de mettre un +1 pour prépa,ENS, IEP
    return parcours

def replace_parcours(df):
    parcours = make_parcours(df)
    dff = df.drop(df.columns[4:18],axis = 1)
    df = pd.concat([dff,parcours],axis = 1)
    return df

def replace_lycee(df):
    dico = {"Lycée public" : 1, "Lycée privé sous contrat": 0}
    df["Vous enseignez en :"].replace(dico,inplace = True)

def replace_choix_ensgn(df):
    dico = {"Autre":0,
            "Non imposé" : 3,
            "Oui, par choix" : 4,
            "Oui, par nécessité":2,
            "Pas pour le moment mais je souhaite le faire d'ici quelques années":1}
    df["Enseignez-vous la spécialité histoire-géographie, géopolitique, sciences politiques ?"].replace(dico,inplace = True)

def replace_volonte_formation(df):
    dico = {"Autre":0,
            "Non et je souhaite demander une formation":2,
            "Non et je ne souhaite pas demander de formation":1,
            "Oui, après avoir commencé à l'enseigner et je n'ai pas demandé cette formation":4,
            "Oui, après avoir commencé à l'enseigner et j’ai demandé cette formation":5,
            "Oui, avant que je l’enseigne et je n'ai pas demandé cette formation":3,
            "Oui, avant que je l’enseigne et j’ai demandé cette formation":6}
    df["Avez-vous reçu une formation à l’enseignement de spécialité ?"].replace(dico,inplace = True)

def replace_theme_prof(df):
    
    """
    
    0 : Première 1 -----> 1
    1 : Première 2 -----> 4
    2 : Première 3 -----> 4
    3 : Première 4 -----> 2.5
    4 : Première 5 -----> 2
   
   
    5 : Terminale 1 ----> 4
    6 : Terminale 2 ----> 3.5
    7 : Terminale 3 ----> 1.5
    8 : Terminale 4 ----> 2.5
    9 : Terminale 5 ----> 3
    10 : Terminale 6 ----> 3
    
    

    
    
    """
    
    liste_poids = [1,4,4,2.5,2,4,3.5,1.5,2.5,3,3]
    
    name_colonnes = df.columns
    liste_name_columns = name_colonnes[9:31]
    
    extract = df[liste_name_columns]
    liste_serie_aise = []
    liste_serie_pas_aise = []
    for i,poids in enumerate(liste_poids):
        #print(liste_name_columns[i])
        liste_serie_aise.append(extract[liste_name_columns[i]].replace({"Oui":poids,"Non":0}))
    for i,poids in enumerate(liste_poids):
        #print(liste_name_columns[11 + i])
        liste_serie_pas_aise.append(extract[liste_name_columns[11 + i]].replace({"Oui":poids,"Non":0}))                         

    somme_theme_aise = sum(liste_serie_aise)
    somme_theme_pas_aise = sum(liste_serie_pas_aise)
    somme_theme_aise.name = "Poids Géopolitique dans Thème aisé"
    somme_theme_pas_aise.name = "Poids Géopolitique dans Thème pas aisé"
    dfff = deepcopy(df)
    df = pd.concat([dfff,somme_theme_aise,somme_theme_pas_aise],axis = 1)
    df = df.drop(df.columns[9:31],axis = 1)
    return df
    

def replace_type_formation(df):
    name_colonnes = df.columns
    liste_name_columns = name_colonnes[8:12]
    extract = df[liste_name_columns]
    """
    0 : Formation initiale        ------->   3
    1 : Formation continue        ------->   1
    2 : Auto-formation            ------->   2
    3 : Pas assez                 ------->  -4
    
    """
    
    FI = extract[liste_name_columns[0]].replace({"Oui":3,"Non":0})
    FC = extract[liste_name_columns[1]].replace({"Oui":1,"Non":0})
    AF = extract[liste_name_columns[2]].replace({"Oui":2,"Non":0})
    PA = extract[liste_name_columns[3]].replace({"Oui":-4,"Non":0})
    
    type_formation = FI + FC + AF + PA
    type_formation.name = "Type Formation"
    dff = df.drop(df.columns[8:12],axis = 1)
    df = pd.concat([dff,type_formation],axis = 1)
    
    return df


def replace_classe(df):
    df["Vous enseignez la spécialité HGGSP en :"].fillna("Non")
    dico = {"Non":0, "en classe de terminale":2,"en classe de première et de terminale":3,"en classe de première":1}
    df["Vous enseignez la spécialité HGGSP en :"].replace(dico,inplace = True)


def replace_pourcentage(df):
    dico1 = {"Entre 20 et 40%":0.3,
             "Plus de 40%":0.5,
             "moins de 20%":0.1}
    dicoT = {"Entre 40 et 80% des élèves de première ont conservé la spécialité HHGSP en terminale" : 0.6,
             "Plus de 80% des élèves de première ont conservé la spécialité HHGSP en terminale":1,
             "moins de 40% des élèves de première ont conservé la spécialité HHGSP en terminale":0.2}
    df["Renseignez le pourcentage d’élèves ayant choisi la spécialité HGGSP en classe de Première dans votre établissement : "].replace(dico1,inplace = True)
    df["Renseignez le pourcentage d’élèves ayant conservé la spécialité HGGSP en classe de Terminale dans votre établissement."].replace(dicoT,inplace = True)
    
    

def replace_methodo(df):
    """
    En fonction du travail des élèves
    
    0 : Recherche en Autonomie : 4
    1 : Recherche en Groupe : 5
    2 : Oral individuel : 1
    3 : Oral en groupe : 2
    4 : Cours Magistral : 0

    """
    liste_poids = [4,5,1,2,0]
    name_colonnes = df.columns
    liste_name_columns = name_colonnes[8:13]
    extract = df[liste_name_columns]
    liste_methodo = []
    for i,poids in enumerate(liste_poids):
       # print(liste_name_columns[i])
        liste_methodo.append(
            extract[liste_name_columns[i]].replace({"Oui":poids,"Non":0}))
    somme_methodo_poids = sum(liste_methodo)
    somme_methodo_poids.name = "Methodologie Poids"
    dff = deepcopy(df)
    df = pd.concat([dff,somme_methodo_poids],axis = 1)
    df = df.drop(df.columns[8:13],axis = 1)
    
    return df
    
def replace_oui_non(df):
    dico = {"Oui":1,"Non":0}
    liste_nom_colonnes = ["L’enseignement de la spécialité influe-t-il sur votre enseignement en tronc commun ? ",
                          "Etablissez-vous une distinction claire entre géopolitique et relations internationales ?",
                          "Souhaitez-vous être tenu informé.e des résultats de cette enquête ? ",
                          "Souhaitez-vous participer à un entretien individuel sur cette thématique ?   Vos impressions, vécus et retours sur l'enseignement de la géopolitique me sont essentiels pour avancer plus aisément dans mes recherches. N'hésitez pas à participer !",
                          "Selon vous, qu’est-ce qui conduit vos élèves à choisir la spécialité HGGSP en classe de Première ?  [Un réel intérêt pour l'histoire-géographie.]",
                          "Selon vous, qu’est-ce qui conduit vos élèves à choisir la spécialité HGGSP en classe de Première ?  [La recherche d'une plus grande culture générale.]",
                          "Selon vous, qu’est-ce qui conduit vos élèves à choisir la spécialité HGGSP en classe de Première ?  [Par stratégie pour les résultats et l'obtention du baccalauréat.]",
                          "Selon vous, qu’est-ce qui conduit vos élèves à choisir la spécialité HGGSP en classe de Première ?  [Par stratégie pour les études supérieures (spécialité recherchée dans les études envisagées).]",
                          "Selon vous, qu’est ce qui conduit vos élèves à conserver la spécialité HGGSP en Terminale ?  [Un intérêt poussé pour la spécialité HGGSP.]",
                          "Selon vous, qu’est ce qui conduit vos élèves à conserver la spécialité HGGSP en Terminale ?  [La volonté de continuer à développer leur culture générale.]",
                          """Selon vous, qu’est ce qui conduit vos élèves à conserver la spécialité HGGSP en Terminale ?  [Par stratégie pour le baccalauréat ("meilleurs" résultats que dans au moins une des deux autres spécialités de première).]""",
                          "Selon vous, qu’est ce qui conduit vos élèves à conserver la spécialité HGGSP en Terminale ?  [Par stratégie pour les études supérieures.]"]
    for nom_colonne in liste_nom_colonnes:
        df[nom_colonne].replace(dico,inplace=True)


def replace_theme_eleve(df):
    
    """
    
    0 : Première 1 -----> 1
    1 : Première 2 -----> 4
    2 : Première 3 -----> 4
    3 : Première 4 -----> 2.5
    4 : Première 5 -----> 2
    5 : Première 6 -----> 0 #Je n'enseigne pas
   
    5 : Terminale 1 ----> 4
    6 : Terminale 2 ----> 3.5
    7 : Terminale 3 ----> 1.5
    8 : Terminale 4 ----> 2.5
    9 : Terminale 5 ----> 3
    10 : Terminale 6 ----> 3
    11 : Terminale 7 -----> 0 #Je n'enseigne pas
     
    
    """
    
    liste_poids_1 = [1,4,4,2.5,2,0]
    liste_poids_T = [4,3.5,1.5,2.5,3,3,0]
    name_colonnes = df.columns
    liste_name_columns_1 = name_colonnes[15:21]
    liste_name_columns_T = name_colonnes[26:33]

    extract_1 = df[liste_name_columns_1]
    extract_T = df[liste_name_columns_T]
    
    
    liste_serie_1 = []
    liste_serie_T = []
    for i,poids in enumerate(liste_poids_1):
        #print(liste_name_columns_1[i])
        liste_serie_1.append(extract_1[liste_name_columns_1[i]].replace({"Oui":poids,"Non":0}))
    for i,poids in enumerate(liste_poids_T):
        #print(liste_name_columns_T[i])
        liste_serie_T.append(extract_T[liste_name_columns_T[i]].replace({"Oui":poids,"Non":0}))                         

    somme_theme_1 = sum(liste_serie_1)
    somme_theme_T = sum(liste_serie_T)
    somme_theme_1.name = "Poids Géopolitique dans Thème préféré élève première"
    somme_theme_T.name = "Poids Géopolitique dans Thème préféré élève terminale"
    dfff = deepcopy(df)
    df = pd.concat([dfff,somme_theme_1,somme_theme_T],axis = 1)
    df = df.drop(liste_name_columns_1,axis = 1)
    df = df.drop(liste_name_columns_T,axis = 1)
    return df
    

def renormalisation(df):
    for column in df:
        df[column] = df[column] /df[column].abs().max()
    return df


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
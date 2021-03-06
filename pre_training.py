# -*- coding: utf-8 -*-
"""

This program was my first program with pandas. 
Hence the form of the function is improving along the program.

"""

import pandas as pd

from copy import deepcopy



def suppr_columns(df):
    """
    

    Parameters
    ----------
    df : dataframe
        It is the dataframe obtained from the answer of french history teacher.

    Returns
    -------
    df : dataframe where all irrelevant (for machine learning) columns are removed

    """
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
    """
    

    Parameters
    ----------
    df : dataframe
        dataframe containing the answer of french history teacher

    Returns
    -------
    
    The function modifies df:
        if age is too important the answer is removed
        if the answer is a string we take the part and convert it into a number.
    
    The data are floored to the minimum age. The youngest will be 0.

    """
    
    nom_colonne_age = df.columns[1]
    colonne_age = df[nom_colonne_age]
    nvx_colonne_age = []
    for age in colonne_age:
        if type(age) != float:
            try:
                if type(age) == str:
                    nvx = age.split(" ")[0]
                    nvx_colonne_age.append(int(nvx))
                else:
                    nvx_colonne_age.append(int(age))
            except:
                #print("Erreur")
                nvx_colonne_age.append(None)
        else:
            nvx_colonne_age.append(None)
    nvx_colonne_age = pd.Series(nvx_colonne_age)
    nvx_colonne_age = nvx_colonne_age - min(nvx_colonne_age)  
    df[nom_colonne_age] = nvx_colonne_age
    
def nettoyage_concours(df):
    """
    

    Parameters
    ----------
    df : data_frame

    Returns
    -------
    None.
    
    The function is similar to the previous one. 
    The oldest teacher now passed his exam at year 0.

    """
    
    nom_colonne_concours = df.columns[3]
    #print(nom_colonne_concours)
    colonne_concours = df[nom_colonne_concours]
    nvx_colonne_concours = []
    for concours in colonne_concours:
        if type(concours) != float:
            try:
                if type(concours) == str:
                    nvx = concours.split(" ")[-1]
                    nvx = int(nvx)
                    if nvx < 22: #For the millenials writing only the two last digits 
                        nvx = nvx + 2000
                    elif nvx < 100: #For those writing only the two last digits
                        nvx = nvx + 1900
                    nvx_colonne_concours.append(int(nvx))
                else:
                    nvx = int(concours)
                    if nvx < 22: #For the millenials writing only the two last digits 
                        nvx = nvx + 2000
                    elif nvx < 100: #For those writing only the two last digits
                        nvx = nvx + 1000
                    nvx_colonne_concours.append(int(nvx))
            except:
                #print("Erreur")
                nvx_colonne_concours.append(None)
        else:
            nvx_colonne_concours.append(None)
    nvx_colonne_concours = pd.Series(nvx_colonne_concours)
    nvx_colonne_concours = nvx_colonne_concours - min(nvx_colonne_concours)
    df[nom_colonne_concours] = nvx_colonne_concours




def replace_gender(df):
    """
    

    Parameters
    ----------
    df : data_frame
    
    Returns
    -------
    This function replace "Un homme" by -1 and "Une femme" by 1. 
    Other answers are replaced by 0

    """
    
    
    dico = {"Un homme" : -1, 
            "Une femme" : 1,
            "Je ne souhaite pas partager cette information":0,
            "Autre":0}
    nom_colonne = df.columns[0]
    #print(nom_colonne)
    df[nom_colonne].replace(dico,inplace=True)


def replace_statut(df):
    """
    

    Parameters
    ----------
    df : data_frame
    
    Returns
    -------
    This function modifies the teacher status by a number in the data frame.
    The metric is the presumed level in geography. 
    Precise metric is given in the dico variable.

    """
    dico = {"Certifi??.e": 1, 
            "Agr??g??.e externe en g??ographie":3, 
            "Agr??g??.e interne":2,
            "Certifi??.e interne": 0.5,
            "Agr??g??.e externe en histoire":2.5,
            "Contractuel.le":0,
            "Autre":0}
    nom_colonne = df.columns[2]
    #print(nom_colonne)
    df[nom_colonne].replace(dico,inplace=True)

def make_parcours(df):
    """
    

    Parameters
    ----------
    df : data_frame

    Returns
    -------
    This function gathers the academic curriculum in columns 4 to 18.
    Then it replaces the value with the number of years needed for the diploma.
    A bonus of +1 is given for ENS or IEP, and +0.5 for CGPE
    It then add columns to the data_frame to be mixed by the next function.

    """
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
    12 : Doctorat G??ographie  
    13 : Doctorat autre
    """
    def prepa(extract,valeur):
        extract_prepa = extract[extract.columns[0:2+1]]
        column_prepa = valeur * extract_prepa.max(axis = 1)
        column_prepa.name = "Pr??pa Oui ou Non"       
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
    #On va choisir arbitrairement de compter le nombre d'ann??es d'??tude et de mettre un +1 pour pr??pa,ENS, IEP
    return parcours

def replace_parcours(df):
    """
    

    Parameters
    ----------
    df : dataframe

    Returns
    -------
    df : dataframe
    
    This function makes the synthetic academic curriculum in a column.
    Then it removes the curriculum columns.
    Finally it add the synthetic column.

    """
    parcours = make_parcours(df)
    dff = df.drop(df.columns[4:18],axis = 1)
    df = pd.concat([dff,parcours],axis = 1)
    return df

def replace_lycee(df):
    """
    

    Parameters
    ----------
    df : dataframe
    
    Returns
    -------
    This function replace Lyc??e public by 1 et Lyc??e priv?? sous contrat by 0.

    """
    dico = {"Lyc??e public" : 1, "Lyc??e priv?? sous contrat": 0}
    df["Vous enseignez en :"].replace(dico,inplace = True)

def replace_choix_ensgn(df):
    """
    

    Parameters
    ----------
    df : dataframe
    
    Returns
    -------
    
    This function modifies the "Enseignez vous la sp?? HGGSP ? " column by 
    value indicated in the dico variable.
    The metric chosen is the willingness to teach the speciality.

    """
    
    dico = {"Autre":0,
            "Non impos??" : 3,
            "Oui, par choix" : 4,
            "Oui, par n??cessit??":2,
            "Pas pour le moment mais je souhaite le faire d'ici quelques ann??es":1}
    df["Enseignez-vous la sp??cialit?? histoire-g??ographie, g??opolitique, sciences politiques???"].replace(dico,inplace = True)

def replace_volonte_formation(df):
    """
    

    Parameters
    ----------
    df : dataframe
    
    Returns
    -------
    
    This function modifies the "Avez vous re??u une formation " column by 
    value indicated in the dico variable.
    The metric chosen is the willingness to be formed.

    """
    dico = {"Autre":0,
            "Non et je souhaite demander une formation":2,
            "Non et je ne souhaite pas demander de formation":1,
            "Oui, apr??s avoir commenc?? ?? l'enseigner et je n'ai pas demand?? cette formation":4,
            "Oui, apr??s avoir commenc?? ?? l'enseigner et j???ai demand?? cette formation":5,
            "Oui, avant que je l???enseigne et je n'ai pas demand?? cette formation":3,
            "Oui, avant que je l???enseigne et j???ai demand?? cette formation":6}
    df["Avez-vous re??u une formation ?? l???enseignement de sp??cialit?????"].replace(dico,inplace = True)

def replace_theme_prof(df):
    """
    

    Parameters
    ----------
    df : dataframe

    Returns
    -------
    df : dataframe
    
    The function gather and replace the difficult/easy (for the teachers) 
    chapters by the value in the following comment. The metric was given by the
    PhD student accordingly to the quantity of geopolitics in the chapter.
    
    We sum all the values of the chapter in one column for easy and one for 
    difficult in order to get a geopolitic difficulty index for the teacher 
    and a geopolitic ease index for the teacher.
    

    """
    
    
    
    """
    
    0 : Premi??re 1 -----> 1
    1 : Premi??re 2 -----> 4
    2 : Premi??re 3 -----> 4
    3 : Premi??re 4 -----> 2.5
    4 : Premi??re 5 -----> 2
   
   
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
    somme_theme_aise.name = "Poids G??opolitique dans Th??me ais??"
    somme_theme_pas_aise.name = "Poids G??opolitique dans Th??me pas ais??"
    dfff = deepcopy(df)
    df = pd.concat([dfff,somme_theme_aise,somme_theme_pas_aise],axis = 1)
    df = df.drop(df.columns[9:31],axis = 1)
    return df
    

def replace_theme_eleve(df):
    """
    

    Parameters
    ----------
    df : dataframe

    Returns
    -------
    df : dataframe
    
    This function is the same as the previous one but for the students.

    """
    
    
    
    """
    
    0 : Premi??re 1 -----> 1
    1 : Premi??re 2 -----> 4
    2 : Premi??re 3 -----> 4
    3 : Premi??re 4 -----> 2.5
    4 : Premi??re 5 -----> 2
    5 : Premi??re 6 -----> 0 #Je n'enseigne pas
   
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
    somme_theme_1.name = "Poids G??opolitique dans Th??me pr??f??r?? ??l??ve premi??re"
    somme_theme_T.name = "Poids G??opolitique dans Th??me pr??f??r?? ??l??ve terminale"
    dfff = deepcopy(df)
    df = pd.concat([dfff,somme_theme_1,somme_theme_T],axis = 1)
    df = df.drop(liste_name_columns_1,axis = 1)
    df = df.drop(liste_name_columns_T,axis = 1)
    return df
    



def replace_type_formation(df):
    """
    

    Parameters
    ----------
    df : dataframe 
    
    Returns
    -------
    df : dataframe
    
    We gather and replace the answer to the style of formation in a column.
    The metric is adding every formation method with an accent to the presumed 
    quantity of information of the method.
    
    The precise quantity is given in the dico variable.
    """
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
    """
    

    Parameters
    ----------
    df : dataframe
    
    Returns
    -------
    This function replaces the classes teached by the professor by a value.
    The metric is sum of the level of the classes. 
    The precise metric is given in the dico variable.

    """
    df["Vous enseignez la sp??cialit?? HGGSP en :"].fillna("Non")
    dico = {"Non":0, 
            "en classe de terminale":2,
            "en classe de premi??re et de terminale":3,
            "en classe de premi??re":1}
    df["Vous enseignez la sp??cialit?? HGGSP en :"].replace(dico,inplace = True)


def replace_pourcentage(df):
    """
    

    Parameters
    ----------
    df : dataframe

    Returns
    -------
    This function replaces the percentage of students going or remaining
    in HGGSP by the mean value of the bracket.

    """
    dico1 = {"Entre 20 et 40%":0.3,
             "Plus de 40%":0.5,
             "moins de 20%":0.1}
    dicoT = {"Entre 40 et 80% des ??l??ves de premi??re ont conserv?? la sp??cialit?? HHGSP en terminale" : 0.6,
             "Plus de 80% des ??l??ves de premi??re ont conserv?? la sp??cialit?? HHGSP en terminale":1,
             "moins de 40% des ??l??ves de premi??re ont conserv?? la sp??cialit?? HHGSP en terminale":0.2}
    df["Renseignez le pourcentage d?????l??ves ayant choisi la sp??cialit?? HGGSP en classe de Premi??re??dans votre ??tablissement :??"].replace(dico1,inplace = True)
    df["Renseignez le pourcentage d?????l??ves ayant conserv?? la sp??cialit?? HGGSP en classe de Terminale dans votre ??tablissement."].replace(dicoT,inplace = True)
    
    

def replace_methodo(df):
    """
    

    Parameters
    ----------
    df : dataframe
    
    Returns
    -------
    df : dataframe
    This function gathers and combine the teaching methodology.
    The metric is the sum of the methodology deployed. The accent is on
    the induced work per student.

    """
    
    """
    En fonction du travail des ??l??ves
    
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
    """
    

    Parameters
    ----------
    df : dataframe

    Returns
    -------
    This function replace "Oui" by 1 and "Non" by 0 in the colonne quoted in
    the liste_nom_colonnes variable.
    

    """
    dico = {"Oui":1,"Non":0}
    liste_nom_colonnes = [
        "L???enseignement de la sp??cialit?? influe-t-il sur votre enseignement en tronc commun?????",
        "Etablissez-vous une distinction claire entre g??opolitique et relations internationales???",
        "Souhaitez-vous ??tre tenu inform??.e des r??sultats de cette enqu??te ???",
        "Souhaitez-vous participer ?? un entretien individuel sur cette th??matique ???  Vos impressions, v??cus et retours sur l'enseignement de la g??opolitique me sont essentiels pour avancer plus ais??ment dans mes recherches. N'h??sitez pas ?? participer !",
        "Selon vous, qu???est-ce qui conduit vos ??l??ves ?? choisir la sp??cialit?? HGGSP en classe de??Premi??re ??? [Un r??el int??r??t pour l'histoire-g??ographie.]",
        "Selon vous, qu???est-ce qui conduit vos ??l??ves ?? choisir la sp??cialit?? HGGSP en classe de??Premi??re ??? [La recherche d'une plus grande culture g??n??rale.]",
        "Selon vous, qu???est-ce qui conduit vos ??l??ves ?? choisir la sp??cialit?? HGGSP en classe de??Premi??re ??? [Par strat??gie pour les r??sultats et l'obtention du baccalaur??at.]",
        "Selon vous, qu???est-ce qui conduit vos ??l??ves ?? choisir la sp??cialit?? HGGSP en classe de??Premi??re ??? [Par strat??gie pour les ??tudes sup??rieures (sp??cialit?? recherch??e dans les ??tudes envisag??es).]",
        "Selon vous, qu???est ce qui conduit vos ??l??ves ?? conserver la sp??cialit?? HGGSP en Terminale ??? [Un int??r??t pouss?? pour la sp??cialit?? HGGSP.]",
        "Selon vous, qu???est ce qui conduit vos ??l??ves ?? conserver la sp??cialit?? HGGSP en Terminale ??? [La volont?? de continuer ?? d??velopper leur culture g??n??rale.]",
        """Selon vous, qu???est ce qui conduit vos ??l??ves ?? conserver la sp??cialit?? HGGSP en Terminale ??? [Par strat??gie pour le baccalaur??at ("meilleurs" r??sultats que dans au moins une des deux autres sp??cialit??s de premi??re).]""",
        "Selon vous, qu???est ce qui conduit vos ??l??ves ?? conserver la sp??cialit?? HGGSP en Terminale ??? [Par strat??gie pour les ??tudes sup??rieures.]"]
    for nom_colonne in liste_nom_colonnes:
        df[nom_colonne].replace(dico,inplace=True)



def renormalisation(df):
    """
    

    Parameters
    ----------
    df : dataframe
    
    Returns
    -------
    df : dataframe
    
    This function renormalizes all the columns between -1 and 1 (or 0 and 1) 
    in order to remove the amplitude dependencies in the Lasso algorithm.

    """
    for column in df:
        df[column] = df[column] /df[column].abs().max()
    return df

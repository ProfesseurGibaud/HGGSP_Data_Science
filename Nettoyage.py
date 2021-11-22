# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 15:44:17 2021

@author: Sylgi
"""


def remove_none(liste):
    liste = liste[1:]
    while None in liste:
        liste.remove(None)
    while "" in liste:
        liste.remove("")
    return liste

def nettoyage_age(liste_age):
    while None in liste_age:
        liste_age.remove(None)
    while "" in liste_age:
        liste_age.remove("")
    
    
    index_error = []
    for i in range(len(liste_age)):
        if type(liste_age[i]) != int:
            try:
                liste_age[i] = int(liste_age[i].split("ans")[0])
            except:
                index_error.append(i)
                #print("erreur")
               
    bonne_liste_age = []
    for i in liste_age:
        if liste_age.index(i) not in index_error:
            bonne_liste_age.append(i)
    bonne_liste_age.sort()
    return bonne_liste_age

def nettoyer_concours(liste_annee_concours):
    #Attention on filtre avec la valeur 96 (prendre l'année du plus vieux et l'enlever)
    liste_annee_concours = remove_none(liste_annee_concours)
    for i in range(len(liste_annee_concours)):
        if type(liste_annee_concours[i]) != int:
            temp_liste = liste_annee_concours[i].split(" ")
            nouvelle_annee = -100
            for item in temp_liste:
                try:
                    nouvelle_annee = int(item)
                except:
                    pass
                    #print("erreur")
            liste_annee_concours[i] = nouvelle_annee
                
    index_96 = liste_annee_concours.index(96)
    liste_annee_concours = liste_annee_concours[index_96 + 1:]
    return liste_annee_concours



    
def de_coord_vers_liste_pourcentage(coordonnee,response_sheet,titre):
    liste_ = [item.value for item in response_sheet[coordonnee]]
    liste_ = remove_none(liste_)
    set_ = set(liste_)
    dico_= {}
    for item in set_:
        nombre_item = int(100*liste_.count(item)/len(liste_))
        dico_[item] = nombre_item
    liste_triee = sorted(dico_.items(), key=lambda t: -t[1])
    with open(titre + ".txt", "w+") as file:
        for item in liste_triee:
            file.write(str(item[0])+","+str(item[1]) + "\n")
    return liste_triee,len(liste_)


def de_sql_vers_liste_pourcentage(colonne_sql,cursor,split_boolean=True):
    sql_sequence = "SELECT {} FROM Reponse".format(colonne_sql)
    cursor.execute(sql_sequence)
    liste_ = []
    for item in cursor:
        liste_.append(item[0])
    n = len(liste_)
    if split_boolean:
        liste_split = []
        for string in liste_:
            liste_string = string.split("/")
            for theme in liste_string:
                liste_split.append(theme)
        liste_ = liste_split
        

    liste_ = remove_none(liste_)
    set_ = set(liste_)
    dico_ = {}
    for item in set_:
        dico_[item] = int(100*liste_.count(item)/len(liste_))

    liste_ordonnee_ = sorted(dico_.items(), key=lambda t: -t[1])
    
    with open(colonne_sql + ".txt","w+") as file:
        for item in liste_ordonnee_:
            file.write(item[0]+","+str(item[1]) + "\n")
            
    return liste_ordonnee_,n




def de_coord_vers_txt(titre,coord,response_sheet):
    liste_ = [item.value for item in response_sheet[coord]]
    liste_ = remove_none(liste_)
    compteur = 0
    with open(titre + " .txt","w+",encoding = "utf-8") as file:
        for item in liste_:
            compteur += 1 
            file.write(str(compteur) +"°) " + item + "\n" + "\n")
    
    
    
    string = ""
    for item in liste_:
        string = string +" " + item
    
    string = string.replace("\n", " ")
    string = string.replace(" de ", " ")
    string = string.replace(" et ", " ")
    string = string.replace(" entre "," ")
    string = string.replace(" la "," " )
    string = string.replace(" le "," ")
    string = string.replace(" des "," ")
    string = string.replace(".Le ",".")
    string = string.replace(" à "," ")
    string = string.replace(" en "," ")
    string = string.replace(" ou "," ")
    string = string.replace(" qui "," ")
    string = string.replace(" une ", " ")
    with open("data.txt","w+",encoding='utf-8') as file:
        file.write(string)
    return string




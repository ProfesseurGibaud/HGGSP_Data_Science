# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 15:47:01 2021

@author: Sylgi
"""



list_column_numeros_exploser = [0,2,3,21,24,26,34,76,88]
list_numeros_supprimer  = [2,18,21,22,23,62,63,66,67,
                           69,92,95]
list_numeros_supprimer = [i-1 for i in list_numeros_supprimer]


def explode_list_columns(list_column_numeros,df):
    columns_names = df.columns
    list_column_names = []
    for num in list_column_numeros:
        list_column_names.append(columns_names[num])
        #print(columns_names[num])
    for nom_colonne in list_column_names:
        data_frame = explode_one_column(nom_colonne,df)
    return data_frame

def explode_one_column(nom_colonne,df):
    colonne = df.pop(nom_colonne)
    names_columns = set(colonne.values)
    for name in names_columns:
        new_column =  [1*(name == data) + 0*(name != data) for data in colonne]
        df.loc[:,name] = new_column
    return df

#df = explode_list_columns(list_column_numeros_exploser,df)




def suppr_columns(list_column_numeros,df):
    columns_names = df.columns
    list_column_names = []
    for num in list_column_numeros:
        list_column_names.append(columns_names[num])
        print(columns_names[num])
    df = df.drop(columns = list_column_names)
    return df
    


df = suppr_columns(list_numeros_supprimer,df)


list_column_numeros = [16,18,46,48,50,52,54,55,56,63,74,83]
df = suppr_columns(list_column_numeros,df)

df = df.replace("Oui",1)
df = df.replace("Non",0)
df = df.dropna(thresh=len(df.columns)-10)



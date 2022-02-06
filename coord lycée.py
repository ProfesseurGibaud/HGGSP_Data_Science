import requests

#Pour ne pas avoir des candidats, il faut enlever les commentaire et la db

#conn = sqlite3.connect('data_full.db')
#cursor = conn.cursor()


import pandas as pd
from pre_training import *


df = pd.read_csv("data_questionnaires.csv",sep = ";")
df = df.drop(columns = ["ID de la réponse","Date de soumission","Dernière page", "Langue de départ","Tête de série", "Date de lancement", "Date de la dernière action"])
names_columns = df.columns



#22 : nom lycée dans colonne 22



def adresse_to_coordonnees(string):
    def string_to_request(string):
        replace = string.replace(" ","+")
        return replace
    url = 'https://nominatim.openstreetmap.org/search.php?q=' + string_to_request(string) + '&format=jsonv2'
    response = requests.get(url)
    if response.json() != []:
        json = response.json()[0]
        latitude  = float(json["lat"])
        longitude = float(json["lon"])
        boolean = True
    else:
        boolean = False
        latitude = 0
        longitude = 0
    return boolean,longitude,latitude

def make_coord(df):
    colonne = df[df.columns[22]]
    for lycee in colonne:
        try:
            boolean,longitude,latitude = adresse_to_coordonnees(lycee)
            if boolean:
                print(longitude,latitude)
        except:
            print("non renseigné")


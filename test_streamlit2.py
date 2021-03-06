# -*- coding: utf-8 -*-
"""Projet Energie_ La consommation d'énergie en France_DA_AVR2021

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xdf5NO-Myg8UO9fo3E9Eqz_e_iP0g-z2

> Germaine BAYONNE

> Emmanuel Gautier

---
> Formation Data_Analyst

> Avril 2021

---

1. Importation des différents paquets
"""

"""# I/ CONTEXTE

Dans le cadre de ce projet dédié à l'étude de la consommation et de la production d'électricité, en France métropolitaine, nous avons utilisé trois bases de données différentes.
En effet, bien que riche, la base de données initiales recensant les consommations et productions d’énergie n’était pas suffisante, nous l’avons donc complétée par deux autres DataFrames contenant des informations relatives à la météo et à la température.
Chacune des bases de données étaient disponibles gratuitement, mais sont pour deux d'entre elles les propriétés d’instances gouvernementales.
Les caractéristiques de chacune d’elles seront listées ci-dessous :

DataFrame 1 - Principal : Données éCO2mix régionales consolidées et définitives (janvier 2013 à septembre 2021) - Propriété de Réseaux de Transport d’Électricité (RTE) via l’application Eco2Mix.

lien d’accès : 
https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-regional-cons-def/information/?disjunctive.libelle_region&disjunctive.nature&sort=-date_heure

Date de téléchargement : 5 août 2021 

Format et volumétrie du fichier au téléchargement : 
CSV, 302 Mo de données 

Période de consommation et de production concernée : 
2013 à 2020 
Les données de l’année en cours n’étant pas complètes nous avons pris le parti de ne pas la prendre en considération afin de ne pas biaiser nos prédictions. L’analyse de base de notre jeux de données a été faite sur toute cette période (soit, 7 ans). Néanmoins, la prédiction n’a été faite en se basant uniquement sur les données de 2016 à 2020.

Nombre de colonnes et lignes : 65 colonnes et 1 787 328 entrées

Le jeu de données est actualisé automatiquement, une fois par jour, et les données sont collectées au pas demi-heure.

On y trouve : 
La consommation réalisée.
La production selon les différentes filières composant le mix énergétique.
La consommation des pompes dans les Stations de Transfert d'Energie par Pompage (STEP).
Le solde des échanges avec les régions limitrophes.

DataFrame 2  : Metéo France données Covid 19 - Propriété de Météo France

Chemin d’accès :
https://drive.google.com/file/d/1HgOVSMumFxkC88vy3nLPGJy5DdEbARmW/view?usp=sharing

date de téléchargement : 22 septembre 2021

Format et volumétrie du fichier au téléchargement :
Format CSV ayant un volume de 5.8 Mo

Période  concernée : du 01/01/2020 au 21/04/2021 (mais prise en compte uniquement jusqu’au 31/12/2020)

Nombre de colonnes et lignes : 26 colonnes et 53 424 lignes

Les colonnes présentes dans le fichier :
Localisation (119 stations en France), Coordonnées GPS, Date du jour et une quantité d’autres indicateurs :

DataFrame 3  : Temperature Quotidienne Régionale - Propriété de data.gouv.fr

Chemin d’accès :
https://drive.google.com/file/d/1YyM4TQbqoxpVfBeDaqOX8NPSleliIg0p/view?usp=sharing

date de téléchargement : 09 octobre 2021 

Format et volumétrie du fichier au téléchargement :
Format CSV ayant un volume de 1.2 Mo

Période de concernée : du 01/01/2016 au 31/08/2021 (mais prise en compte uniquement jusqu’au 31/12/2019 pour Machine Learning, pour pouvoir prévoir 2020)

Nombre de colonnes et lignes : 6 colonnes et 26 897 lignes

Les colonnes présentes dans le fichier sont : 
Date, 
Code INSEE Région, 
Région, 
Températures Minimale, 
Maximale 
Moyenne


"""



import streamlit as st

add_selectbox = st.sidebar.selectbox(
    "Eléments à visualiser",
    ("Contexte","Nettoyage et Gestion de données","DataVisualisation","ML - Preparation Donnees","ML - Test différents modèles")
)

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd 
import numpy as np
import streamlit as st
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge, LassoCV

from sklearn import model_selection
from sklearn.model_selection import cross_val_predict, cross_validate
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
# %matplotlib inline

import seaborn as sns 
import matplotlib.pyplot as plt
# %matplotlib inline
#from google.colab import drive


nrj = pd.read_csv('eco2mix-regional-cons-def.csv', sep = ';')

"""Affichage de la taille (initiale) de la BDD principale (Ecomix) : Nbre lignes * Nbre colonnes"""

#affichage de la dimension de la BDD
nrj.shape

#aperçu des données par le bas pour avoir une idée globale de la distribution des données
#NaNs beaucoup trop important via head()

nrj.tail()

#affichage des informations de base de la BDD 
nrj.info()

#Description statistiques 
nrj.describe()

#AFfichage des valeurs uniques de chaque colonne
for variable in nrj:
    print(str(variable), '-', nrj[str(variable)].unique())

"""# II/ NETTOYAGE ET GESTION DE DONNEES (Affichage de la répartition statistique des données pour la consommation et chaque mode de production)

---



"""

#suppression des colonnes Flux + date-heure + TCO / TCH 
nrj_new = nrj.drop(labels = ['Date - Heure','TCO Thermique (%)', 'TCH Thermique (%)','TCO Nucléaire (%)',
                             'TCH Nucléaire (%)', 'TCO Eolien (%)','TCH Eolien (%)','TCO Solaire (%)','TCH Solaire (%)', 'TCO Hydraulique (%)',
                            'TCH Hydraulique (%)','TCO Bioénergies (%)','TCH Bioénergies (%)', 'Ech. physiques (MW)','Column 26'], axis = 1)

#affihage des valeurs uniques du nouveau DataFrame
nrj_new.nunique()

#affichage des étendues des valeurs de chq colonne 
#colonnes séparées des valeurs par un '-'

for variable in nrj_new:
    print(str(variable), '-', nrj_new[str(variable)].unique())



fig1 = plt.figure(figsize=[20, 10])
#st.pyplot()

#plt.subplot(331)
#sns.boxplot(nrj_new['Consommation (MW)'])
#st.pyplot()

plt.subplot(331)
sns.boxplot(nrj_new['Consommation (MW)'])


plt.subplot(332)
sns.boxplot(nrj_new['Thermique (MW)'])


plt.subplot(333)
sns.boxplot(nrj_new['Nucléaire (MW)'])


plt.subplot(334)
sns.boxplot(nrj_new['Eolien (MW)'])


plt.subplot(335)
sns.boxplot(nrj_new['Solaire (MW)'])


plt.subplot(336)
sns.boxplot(nrj_new['Hydraulique (MW)'])


plt.subplot(337)
sns.boxplot(nrj_new['Pompage (MW)'])


plt.subplot(338)
sns.boxplot(nrj_new['Bioénergies (MW)']);


st.pyplot(fig1)


#Gestion des NaN pour les variables 'Consommations' et des 'différents types de production"
nrj_new['Consommation (MW)'].fillna(nrj_new['Consommation (MW)'].median(), inplace = True)

nrj_new['Thermique (MW)'].fillna(0, inplace = True)
nrj_new['Nucléaire (MW)'].fillna(0, inplace = True)
nrj_new['Eolien (MW)'].fillna(0, inplace = True)
nrj_new['Solaire (MW)'].fillna(0, inplace = True)
nrj_new['Hydraulique (MW)'].fillna(0, inplace = True)
nrj_new['Pompage (MW)'].fillna(0, inplace = True)
nrj_new['Bioénergies (MW)'].fillna(0, inplace = True)

#100 * nrj_new.isnull().sum() / len(nrj_new)

#"""3. Ajustement des colonnes pour faciliter la visualisation des données"""

#Créaton de 3 colonnes (Année, mois, jour) à partir de la colonne date
#définition de fonction permettant le découpage de la colonne date 



def get_month(Date):
    return Date.split('-')[1]

def get_day(Date):
    return Date.split('-')[2]
    

months = nrj_new['Date'].apply(get_month)
days = nrj_new['Date'].apply(get_day)


nrj_new['mois'] = months
nrj_new['jour'] = days

nrj_new.head()

#modification du type des colonnes nouvellement créées
nrj_new['jour'] = nrj_new['jour'].astype('int')
nrj_new['mois'] = nrj_new['mois'].astype('int')


#Suppression des lignes année 2021 (car incomplètes)
#nrj = nrj_new[nrj_new['Année'] == 2021 ].index
#nrj_new.drop(nrj , inplace=True)

#modification du format de la colonne date qui est jusque-là de type object
nrj_new['Date']= pd.to_datetime(nrj_new['Date'])

#Définition d'une fonction permettant de supprimer l'élément ':' sur la colonne 'Heure'
#L'idée étant de convertir ensuite la colonne 'Heure'en float plutot que object

def Hour (Heure):
    return Heure.split(':')[0]

Hours = nrj_new['Heure'].apply(Hour)

nrj_new['Heure24'] = Hours

nrj_new['Heure24'] = nrj_new['Heure24'].astype(float)

#suppression des lignes Nan Conso
nrj_new.drop(nrj_new.loc[nrj_new['Consommation (MW)'].isna()].index,inplace = True)

#suppression de la colonne 'Heure'
nrj_new.drop('Heure', axis = 1, inplace=True)

nrj_new.info()

#Quelle est la consommation d'énergie par région
nrj_total = nrj_new['Consommation (MW)'].groupby(nrj_new['Région']).sum()

#df.groupby('A').agg(['min', 'max'])
print(nrj_total)

nrjtherm = nrj_new['Thermique (MW)'].groupby(nrj_new['Région']).sum()
nrjnucl= nrj_new['Nucléaire (MW)'].groupby(nrj_new['Région']).sum()
nrjeol = nrj_new['Eolien (MW)'].groupby(nrj_new['Région']).sum()
nrjsol = nrj_new['Solaire (MW)'].groupby(nrj_new['Région']).sum()
nrjhyd = nrj_new['Hydraulique (MW)'].groupby(nrj_new['Région']).sum()
nrjpomp = nrj_new['Pompage (MW)'].groupby(nrj_new['Région']).sum()
nrjbio = nrj_new['Bioénergies (MW)'].groupby(nrj_new['Région']).sum()

#Et ainsi de suite

print(nrjtherm)


print(nrjnucl)

print(nrjeol)

nrj_new['Production (MW)']= nrj_new['Thermique (MW)'] + nrj_new['Nucléaire (MW)'] + nrj_new['Eolien (MW)'] + nrj_new['Solaire (MW)'] + nrj_new['Hydraulique (MW)'] + nrj_new['Pompage (MW)'] + nrj_new['Bioénergies (MW)']

"""# III/ DATA VISUALIZATION (DATAVIZ')

---

***ETUDE GENERALE***

1. Matrice de corrélation
"""

#visualisation des corrélations entre chaque variables 




fig_corr, ax = plt.subplots(figsize=(15,15))
matrice_de_corrélation = nrj_new.corr()
sns.heatmap (matrice_de_corrélation, annot = True, ax = ax, cmap = "YlGnBu" );
st.pyplot(fig_corr)
"""Corrélation entre la variable 'consommation' et 'bioénergies' mais cette corrélation est plutôt faible (0.62). 
Cela signifie t-il que la consommation est plus ou moins importante selon que l'énergie consommées est de catégorie bioénergétique ? La variable 'bioénergies' est la seule corrélée à la variable cible.

On peut aussi noter que la variable 'Code INSEE région' est corrélée aux variables 'Hydraulique (MW)' (0.61). cela signifie-t-il que : 
Selon la région, la production hydraulique  est plus ou moins importante ?

2. Quelle est la consommation générale (courbe de densité) ? 


---
"""

# Affichage d'une courbe de densité Kernel





fig_conso = plt.figure(figsize=[20, 10])
#st.pyplot()
plt.subplot(111)
sns.kdeplot(nrj_new['Consommation (MW)']);
st.pyplot(fig_conso)

"""3. Quelle est, par type, la production générale? (courbe de densité) """

#Analyse de la distribution des variables de production 

fig_energies = plt.figure(figsize=[20, 10])

plt.subplot(331)
sns.kdeplot(nrj_new['Thermique (MW)']);

plt.subplot(332)
sns.kdeplot(nrj_new['Nucléaire (MW)']);


plt.subplot(333)
sns.kdeplot(nrj_new['Eolien (MW)']);


plt.subplot(334)
sns.kdeplot(nrj_new['Solaire (MW)']);


plt.subplot(335)
sns.kdeplot(nrj_new['Hydraulique (MW)']);

plt.subplot(336)
sns.kdeplot(nrj_new['Pompage (MW)']);


plt.subplot(337)
sns.kdeplot(nrj_new['Bioénergies (MW)']);


st.pyplot(fig_energies)

#Visualisation de la distribution des données pour la variable "Consommation (MW) et sa densité de probabilité

fig_distrib = plt.figure(figsize=[25, 10])
plt.subplot(131)
sns.violinplot(nrj_new['Région'], nrj_new['Consommation (MW)']);
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['ARA','BFC','BR','CVL','GE','HDF','NOR','NA','OC','PDL','PACA','IDF']);

plt.title('Distribution et densité de la variable consommation (MW)par Région')


"""

---


***ETUDE APPROFONDIE :***

4. Quelle est la consommation générale par région (Quelles sont les régions les plus consommatrices d'énergie)? """
plt.subplot(132)
sns.barplot(x = 'Consommation (MW)', y = 'Région', data = nrj_new);
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11], ['ARA','BFC','BR','CVL','GE','HDF','NOR','NA','OC','PDL','PACA','IDF']);

"""Sur la base de cet histogramme certaines régions sont beaucoup plus consommatrices d'énergie que d'autres. La région Ile-de-France est largement en tête de liste en matière de consommation d'énergie. En deuxième puis en troisième position viennent les régions Auvergne-Rhône-Alpes et Grand-Est. 

Ce niveau de consommation plus élévée dans ces régions s'expliquent probablement par le fait que la population dans ces régions sont parmis les plus élévées (IDF - 12 326 429, ARA - 8 092 598, GE - 5 524 817 contre CVL - 2 562 431). 

En revanche la taille de la population, n'explique pas tout car pour la Région Occitanie, qui compte une population légèrement plus élevée que la région Grand-Est (5 524 817 vs 5 985 751) consomme moins que cette dernière. Le Grand-Est étant au nord de la France, contre le sud de la France la région Occitanie, on peut facilement supposer que le climat est un facteur non négligeable des différences de consommations d'une région à une autre.

Bien entendu, d'autre facteur peuvent expliquer ces différences, tels que le mode de vie dans une région donnée.

5. Quelle est la production générale par région (Quelles sont les régions les plus productrices d'énergie)?
"""
plt.subplot(133)
sns.barplot(x = 'Production (MW)', y = 'Région', data = nrj_new);
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11], ['ARA','BFC','BR','CVL','GE','HDF','NOR','NA','OC','PDL','PACA','IDF']);
st.pyplot(fig_distrib)

"""On peut constater que la région Auvergne-Rhône-Alpes est la plus productrice d'énergie en France, suivie de près par la Région Grand-Est. On sait que la region ARA represente à elle seule 23% de la production nationale selon les infos de la RTE. 
  
  La région Normandie produit très peu d'énergie (environ 500 MW) mais pour autant est celle qui en consomme le plus d'énergie.

---

6.   Quelle est la production d'énergie par filière  et par région (Quels sont les régions qui produisent le plus d'énergie (par types) : 
  *  Thermique
  *  Nucléaire
  *  Eolien
  *  Solaire
  *  hydraulique
  *  Bioénergies
  *  Pompage

"""

fig_filiere_1 = plt.figure(figsize=[20,10])


plt.subplot(331)
sns.barplot(x="Thermique (MW)", y="Région", data=nrj_new);
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11], ['ARA','BFC','BR','CVL','GE','HDF','NOR','NA','OC','PDL','PACA','IDF']);



plt.subplot(332)
sns.barplot('Nucléaire (MW)', 'Région', data=nrj_new);
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11], ['ARA','BFC','BR','CVL','GE','HDF','NOR','NA','OC','PDL','PACA','IDF']);



plt.subplot(333)
sns.barplot('Eolien (MW)','Région', data=nrj_new);
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11], ['ARA','BFC','BR','CVL','GE','HDF','NOR','NA','OC','PDL','PACA','IDF']);


plt.subplot(334)
sns.barplot('Solaire (MW)','Région', data = nrj_new);
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11], ['ARA','BFC','BR','CVL','GE','HDF','NOR','NA','OC','PDL','PACA','IDF']);



plt.subplot(335)
sns.barplot('Hydraulique (MW)', 'Région', data = nrj_new);
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11], ['ARA','BFC','BR','CVL','GE','HDF','NOR','NA','OC','PDL','PACA','IDF']);


plt.subplot(336)

sns.barplot('Bioénergies (MW)', 'Région', data = nrj_new);
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11], ['ARA','BFC','BR','CVL','GE','HDF','NOR','NA','OC','PDL','PACA','IDF']);

plt.subplot(337)
sns.barplot('Pompage (MW)', 'Région', data = nrj_new);
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11], ['ARA','BFC','BR','CVL','GE','HDF','NOR','NA','OC','PDL','PACA','IDF']);

st.pyplot(fig_filiere_1)


"""***Production d'énergie thermique*** : 
la région Bourgogne-Franche-Comté (BFC) est celle qui produit le plus d'énergie thermique (environ 1100 mw). Mais celle-ci est suivie de près par les régions Pays de Loire (PDL) & Provence-Alpes-Cote d'Azur (PACA).

***Production d'energie Nucléaire*** : 
En matière de production nucléaire, l'Occitanie (OC) et une fois de plus la BFC sont les régions les plus productrices d'énergie. Le Grand-Est (GE) en est également un grand producteur en France.

***Production d'énergie Eolien*** :
La production Eolienne est produite en majorité par les régions PDL et BFC.

***Production d'énergie Solaire*** : 
Cette fois-ci, ce sont les régions Ile-de-France (IDF - 275MW) et Hauts-de-France (HDF - 225MW) qui produisent le plus d'énergie solaire sur le territoire national.

***Production d'énergie Hydraulique et par Pompage*** :
L'Occitanie (OC) produit le plus d'énergie hydraulique et procède beaucoup par transfert d'énergie par pompage ou STEP. Les HDF et la BFC également.

***Production de Bioénergies*** : 
Contrairement aux autres types de production, les bioénergies sont produites, certes à des degrés differents selon la région mais, sont partout. La région la plus productrice de bioénergies est la région Ile-de-France soit 160MW, qui est suivi de près par la région Normandie (140MW)
************************************

Alors que la région Auvergne-Rhônes-Alpes est celle qui produit à priori le plus d'énergie sur le teritoire national, nous pouvons constater sur ces graphiques que la région ARA n'apparaît pas parmi les régions les plus productrices d'énergie. 
Est-ce dû à une difficulté de collecte des données pour cette région ?

---

---


# IV/ **MACHINE LEARNING - PREPARATION DES DONNEES**




---

1. Préparation de données pour enrichir notre BDD initiale :

1.1 ajout des données :


*   Données Historiques météo
"""



"""  1.2 lecture de la BDD météo & température"""

meteo = pd.read_csv('meteo-france-donneesq-covid19.csv', sep = ';', engine = 'python', encoding='latin1')
#temperature = pd.read_csv('')

temperature_2016_a_2020 = pd.read_csv('temperature-quotidienne-regionale.csv', sep = ';', encoding='latin1')

"""1.3 Nettoyage des BDD météo & température

> 1.3.1 Nettoyage BDD Météo


"""

meteo['TM'] = meteo['TM'].str.replace(',','.')

meteo.isna().sum() #Verification des NaN

meteo['TM'].fillna(meteo['TM'].median(),inplace = True)
#On remplace les NaN de la température moyenne (la seule qui nous intéresse) par la valeur médiane

meteo.isna().sum()

meteo.head()

meteo['TM'] = meteo['TM'].astype(float)
meteo.TM.dtype

meteo = meteo.rename(columns = {'DATE':'Date'})
meteo['Date'].dtype
meteo['Date']=meteo['Date'].astype(str)

meteo.groupby("Date").mean()

#On enlève toutes les colonnes sauf "Date" et "TM" (température moyenne)

meteo = meteo.drop("POSTE", axis = 1)
meteo = meteo.drop("ALT", axis = 1)
meteo = meteo.drop("UN", axis = 1)
meteo = meteo.drop("UX", axis = 1)
meteo = meteo.drop("DHUMI40", axis = 1)
meteo = meteo.drop("DHUMI80", axis = 1)
meteo = meteo.drop("NOM", axis = 1)
meteo = meteo.drop("LON", axis = 1)
meteo = meteo.drop("LAT", axis = 1)
meteo = meteo.drop("RR", axis = 1)
meteo = meteo.drop("QRR", axis = 1)
meteo = meteo.drop("TN", axis = 1)
meteo = meteo.drop("QTN", axis = 1)
meteo = meteo.drop("TX", axis = 1)
meteo = meteo.drop("QTX", axis = 1)
meteo = meteo.drop("QTM", axis = 1)
meteo = meteo.drop("FFM", axis = 1)
meteo = meteo.drop("QFFM", axis = 1)
meteo = meteo.drop("QUN", axis = 1)
meteo = meteo.drop("QUX", axis = 1)
meteo = meteo.drop("QDHUMI40", axis = 1)
meteo = meteo.drop("QDHUMI80", axis = 1)
meteo = meteo.drop("QUM", axis = 1)
meteo = meteo.drop("UM", axis = 1)

meteo.head()
#Température moyenne en fonction de la journée

nrj_new['Date'] = nrj_new['Date'].astype(str)
nrj_new['Date'] = nrj_new['Date'].str.replace('-','')
nrj_new.groupby('Date').mean()

"""> 1.3.2 Nettoyage de la BDD temperature


"""

#On récupère les températures de 2016 à 2020
temperature_2016_a_2020['date'] = temperature_2016_a_2020['date'].str.replace('-','')
temperature_2016_a_2020 = temperature_2016_a_2020.rename(columns = {'date':'Date'})

temperature_2016_a_2020.isna().sum() #Aucune Nan dans le fichier temperature de 2016 à 2020
temperature_2016_a_2020.duplicated().sum() #Aucun doublon dans le fichier temperature de 2016 à 2020

temperature_2016_a_2020 = temperature_2016_a_2020.groupby("Date").mean()
temperature_2016_a_2020 = temperature_2016_a_2020.drop("code_insee_region", axis=1) #On ne garde que les températures min, max et moyenne
temperature_2016_a_2020.head()


"""1.4 Fusion des BDD (meteo et Conso) pour affichage Corrélation"""

meteo_df = meteo.groupby("Date").mean()
Conso_df = nrj_new.groupby("Date").mean()

Conso_et_meteo_2020 =meteo_df.merge(Conso_df,left_index=True,right_index=True)

Conso_et_meteo_2020 = Conso_et_meteo_2020.drop("Heure24", axis=1)
Conso_et_meteo_2020 = Conso_et_meteo_2020.drop("Code INSEE région", axis=1)
Conso_et_meteo_2020 = Conso_et_meteo_2020.drop("mois", axis=1)
Conso_et_meteo_2020 = Conso_et_meteo_2020.drop("jour", axis=1)
Conso_et_meteo_2020.head()

"""2. visualisation des corrélations entre chaque variables """
fig_mat, ax = plt.subplots(figsize=(20,20))
mat_de_corr = Conso_et_meteo_2020.corr()
sns.heatmap (mat_de_corr, annot = True, ax = ax, cmap = "inferno" );
st.pyplot(fig_mat)

"""Cette matrice de correlation laisse supposer qu'il y a une corrélation entre les températures et la consommation électrique.
En effet, entre "TM" et "Consommation (MW)" le coefficient est de -0.8. Cela indique une corrélation négative.
A savoir : Plus la température est basse, plus la consommation est élevée"""


nrj_new.head()
#On prend les données de consommation (uniquement) du dataframe original (2013 à 2020)
Conso_2013_a_2020= nrj_new.groupby('Date').mean()
Conso_2013_a_2020 = Conso_2013_a_2020['Consommation (MW)']
Conso_2013_a_2020.head()

temperature_et_conso_2016_a_2020 = temperature_2016_a_2020.merge(Conso_2013_a_2020,left_index=True,right_index=True)
temperature_et_conso_2016_a_2020.head()
#On fusionne en ne gardant que les valeurs de 2016 à 2020 (car pas d'historique avant 2020 pour la température)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
norm = scaler.fit_transform(temperature_et_conso_2016_a_2020) #plutôt que norm = scaler.fit_transform(Conso_et_meteo_2020)
#Normalisation des données

temperature_et_conso_2016_a_2020.info()

"""# V/ TEST DE DIFFERENTS MODELES DE MACHINE LEARNING"""

"""Machine learning sur les données de 2016 à 2019 (pour pouvoir prédire 2020)"""

"""1. Mesure de l'influence des variables grâce à une régression linéaire (températures en abscisses (°C), Consommation en ordonnées (MW))
"""

#Utilisation de la régression linéaire sur les données de 2016 à 2019


#fig, ax = plt.subplots(figsize=(20,20))
fig_temp_conso = plt.figure(figsize=(10, 8))
plt.scatter(temperature_et_conso_2016_a_2020['tmoy'], temperature_et_conso_2016_a_2020['Consommation (MW)'], color='darkblue');
st.pyplot(fig_temp_conso)

plt.xlabel('Température');
plt.ylabel('consommation en MW')

plt.title('2016 à 2020');

#Construction d'un modèle de régression linéaire grâce à la classe LinearRegression du sous module sklearn.linear_model.

Consommation = temperature_et_conso_2016_a_2020['Consommation (MW)']
Tempmoyenne = temperature_et_conso_2016_a_2020[['tmoy']]

slr = LinearRegression()
slr.fit(Tempmoyenne, Consommation)

#fig_temp_linear_regression = plt.figure(figsize=(10, 8))
#print(slr.intercept_)
#print(slr.coef_)
#st.pyplot(fig_temp_linear_regression)

cross_validate(slr, Tempmoyenne, Consommation, return_train_score=True, cv=4)

cross_validate(slr, Tempmoyenne, Consommation, return_train_score=True, cv=4)['test_score'].mean()

pred_conso = slr.predict(Tempmoyenne)
residus = pred_conso - Consommation
residus.describe()

"""2. Ajout d'une droite de régression estimée sur le nuage de points obtenu précédemment (températures en abscisses (°C), Consommation en ordonnées (MW))"""

fig_temp_moyenne = plt.figure(figsize=(10, 8))
plt.scatter(Tempmoyenne['tmoy'], Consommation, color='darkblue')
plt.plot(Tempmoyenne, pred_conso ,color='k');
st.pyplot(fig_temp_moyenne)

plt.xlabel('Température');
plt.ylabel('consommation en MW')

plt.title('2016 à 2019');

"""Il semble y avoir un lien entre consommation et température moyenne (jusqu'à 20°C)

La droite de régression semble raisonnablement ajustée"""

#Gestion des Nans
#calcule du nombre de colonnes ayant des valeurs manquantes 
print('il y\'a', temperature_et_conso_2016_a_2020.isna().any(axis=0).sum(), 'colonnes sur 12 ayant des valeurs manquantes')

#calcule de la somme totale des valeurs manquantes
print('avec un total de', temperature_et_conso_2016_a_2020.isna().sum(), 'de valeurs manquantes')

temperature_et_conso_2016_a_2020 = temperature_et_conso_2016_a_2020.reset_index()


temperature_et_conso_2016_a_2020[temperature_et_conso_2016_a_2020.columns] = pd.DataFrame(preprocessing.StandardScaler().fit_transform(temperature_et_conso_2016_a_2020))


target = temperature_et_conso_2016_a_2020['Consommation (MW)']
data = temperature_et_conso_2016_a_2020.drop('Consommation (MW)', axis = 1)


X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=789)


#X_train = X_train.values.astype(np.float)
#y_train = y_train.values.astype(np.float)

from sklearn.linear_model import RidgeCV

#X_train.values.reshape(-1, 1)
#y_train.values.reshape(-1, 1)

ridge_reg = RidgeCV(alphas= (0.001, 0.01, 0.1, 0.3, 0.7, 1, 10, 50, 100))
ridge_reg.fit(X_train, y_train)

#a utiliser (cf. Jeremy)
#fig_ridge = plt.figure(figsize=[20, 10])
#print('alpha sélectionné par c-v :', ridge_reg.alpha_)
#print('score train :', ridge_reg.score(X_train, y_train))
#print('score test :', ridge_reg.score(X_test, y_test))
#st.pyplot(fig_ridge)

ridge_pred_train = ridge_reg.predict(X_train)
ridge_pred_test = ridge_reg.predict(X_test)

#fig_ridge2 = plt.figure(figsize=[20, 10])
#print('mse train :', mean_squared_error(ridge_pred_train, y_train))
#print('mse test :', mean_squared_error(ridge_pred_test, y_test))
#st.pyplot(fig_ridge2)

"""3. Machine learning avec LassoCV"""

#Machine Learning avec Lasso
from sklearn.linear_model import Lasso

fig_lasso = plt.figure(figsize=[20, 10])

lasso_r = Lasso(alpha=1)

lasso_r.fit(X_train, y_train)

#lasso_r.coef_

lasso_reg = Lasso(alpha=0.1)

lasso_reg.fit(X_train, y_train)

lasso_coef = lasso_reg.coef_

plt.plot(range(len(data.columns)), lasso_coef)
plt.xticks(range(len(data.columns)), data.columns.values, rotation=70);

print('score train :', lasso_reg.score(X_train, y_train))
print('score test :', lasso_reg.score(X_test, y_test))
st.pyplot(fig_lasso)

lasso_pred_train = lasso_reg.predict(X_train)
lasso_pred_test = lasso_reg.predict(X_test)

#fig_lasso2 = plt.figure(figsize=[20, 10])
#print('mse train :', mean_squared_error(lasso_pred_train, y_train))
#print('mse test :', mean_squared_error(lasso_pred_test, y_test))
#st.pyplot(fig_lasso2)



from sklearn.linear_model import lasso_path

mes_alphas = (0.001, 0.01, 0.02, 0.025, 0.05, 0.1, 0.25, 0.5, 0.8, 1.0)

alpha_path, coefs_lasso, _ = lasso_path(X_train, y_train, alphas=mes_alphas)

coefs_lasso.shape

import matplotlib.cm as cm

fig_lasso_ML = plt.figure(figsize=[10, 7])
#plt.figure(figsize=(10, 7))

for i in range(coefs_lasso.shape[0]):
    plt.plot(alpha_path, coefs_lasso[i,:], '--')

plt.xlabel('Alpha')
plt.ylabel('Coefficients')
plt.title('Lasso path');
st.pyplot(fig_lasso_ML)

from sklearn.linear_model import LassoCV

model_lasso = LassoCV(cv=10).fit(X_train, y_train)

alphas = model_lasso.alphas_

fig_lassoCV = plt.figure(figsize=(10, 8))


plt.plot(alphas, model_lasso.mse_path_, ':')
plt.plot(alphas, model_lasso.mse_path_.mean(axis=1), 'k', label='Moyenne', linewidth=2)

st.pyplot(fig_lassoCV)

plt.axvline(model_lasso.alpha_, linestyle='--', color='k', label='alpha : estimation CV')

plt.xlabel('Alpha')
plt.ylabel('Mean square error')
plt.title('Mean square error pour chaque échantillon')
plt.legend();

pred_test = model_lasso.predict(X_test)

print('score test :', model_lasso.score(X_test, y_test))
print('mse test :', mean_squared_error(pred_test, y_test))

"""4. Machine Learning avec ElasticNetCV"""

#Machine Learning avec Elastic Net

from sklearn.linear_model import ElasticNetCV

model_en = ElasticNetCV(cv=8, l1_ratio=(0.1, 0.25, 0.5, 0.7, 0.75, 0.8, 0.85, 0.9, 0.99), 
                        alphas=(0.001, 0.01, 0.02, 0.025, 0.05, 0.1, 0.25, 0.5, 0.8, 1.0))

model_en.fit(X_train, y_train)
#model= LassoCV(cv=10).fit(X_train, y_train)

coeffs = list(model_en.coef_)
coeffs.insert(0, model_en.intercept_)
feats = list(data.columns)
feats.insert(0, 'intercept')

pd.DataFrame({'valeur estimée': coeffs}, index=feats)

alphas = model_en.alphas_

fig_ElasticNet = plt.figure(figsize=(10, 10))


for i in range(model_en.mse_path_.shape[0]) :
    plt.plot(alphas, model_en.mse_path_[i,:,:].mean(axis=1),
             label='Moyenne pour l1_ratio= %.2f' %model_en.l1_ratio[i], linewidth=2)

plt.xlabel('Alpha')
plt.ylabel('Mean squared error')
plt.title('Mean squared error pour chaque $\lambda$')
plt.legend();

pred_train = model_en.predict(X_train)
pred_test = model_en.predict(X_test)
print(np.sqrt(mean_squared_error(y_train, pred_train)))
print(np.sqrt(mean_squared_error(y_test, pred_test)))



print('score train :', model_en.score(X_train, y_train))
print('score test :', model_en.score(X_test, y_test))



moy = scaler.mean_[-1]
ec = scaler.scale_[-1]
print('moyenne :', moy)
print('ecart-type :', ec)


pd.DataFrame({'Consommation observée': (y_test*ec)+moy, 'Consommation prédite' : np.round((pred_test*ec)+moy)}, 
             index=X_test.index).head(7)

st.pyplot(fig_ElasticNet)

"""5. Machine Learning avec Random Forest Regressor"""

#importation des modules nécessaires 

from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import load_boston
from sklearn.datasets import make_regression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt
from sklearn import set_config

#Séparer les données en un ensemble d'apprentissage (X_train, y_train) 
#et un ensemble de test (X_test, y_test) contenant 20% des données

X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=789)

#définition du modèle en utilisant la classe RandomForestRegressor

rfr = RandomForestRegressor()
print(rfr)

#adaptation du modèle aux données du l'entrainement et vérification du score de précision du modèle

rfr.fit(X_train, y_train)

score = rfr.score(X_train, y_train)
print("R-squared:", score)


#vérification de l'exactitude des données prédites en utilisant les métriques MSE et RMSE

ypred = rfr.predict(X_test)
mse = mean_squared_error(y_test, ypred)
print("MSE: ", mse)
print("RMSE: ", mse*(1/2.0))


#visualization des données initiales vs predites via un plot 

fig_randomforest_regressor = plt.figure(figsize=[20, 10])
x_ax = range(len(y_test))
plt.plot(x_ax, y_test, linewidth=1, label="original")
plt.plot(x_ax, ypred, linewidth=1.1, label="predicted")
plt.title("y-test and y-predicted data")
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend(loc='best',fancybox=True, shadow=True)
plt.grid(True)
plt.show()

st.pyplot(fig_randomforest_regressor)


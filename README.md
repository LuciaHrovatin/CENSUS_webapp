# C.E.N.S.U.S 
## Calculator of Earnings Nationally Scored via User Specifics
___

The C.E.N.S.U.S. project has been developed as final assignment of the Big Data Technologies course, offered by the University of Trento. 

## Project objective 
The project objective refers to deploying a web application, taking as input specific user data and returning a prediction of his/her income group, subcategorizing the Irpef system of taxation and its income segmentation. The prediction corresponds to the output of a Random Forest model trained with data provided by the Banca d’Italia and by the Sole24ore.
Specifically, the datasets employed are: 

- Banca d'Italia, Indagine sui bilanci delle famiglie italiane, [Indagine sul 2016](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/ricerca/ricerca.html?min_anno_pubblicazione=2018&max_anno_pubblicazione=2018) whose data refers to the 2016 survey 

- Banca d'Italia, Indagine sui bilanci delle famiglie italiane, [Indagine sul 2014](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/ricerca/ricerca.html?min_anno_pubblicazione=2015&max_anno_pubblicazione=2015) with data referring to the survey of 2014

- Lab24: [Qualità della vita](https://lab24.ilsole24ore.com/qualita-della-vita/) 

Whereas the Banca d’Italia offered a large amount of data, only three datasets were of interest for this project's scope: carcom, rper, rfam. Their description, along with the description of their variables, can be found on the relative site.       

# NUTS2 - Istat code for region of residence:

1=Piemonte, 
2=Valle d'Aosta,
3=Lombardia, 
4=Trentino, 
5=Veneto,
6=Friuli, 
7=Liguria,
8=Emilia Romagna,
9=Toscana,
10=Umbria,
11=Marche,
12=Lazio, 
13=Abruzzo,
14=Molise,
15=Campania,
16=Puglia,
17=Basilicata,
18=Calabria,
19=Sicilia, 
20=Sardegna

# VARIABILI nella tabella "FINAL" ovvero l'unione di 2016-2014 (dal 2014 provengono solo le fam che poi hanno abbandonato il questionario) 
 
NQUEST and NORD: The primary key to merge household level information is NQUEST (household ID). 
NQUEST must be considered together with NORD (ID of each household member) to merge individual level 
information. 

NCOMP: numero di componenti per famiglia 

SEX: maschio 1, femmina 2 

ANASC: anno di nascita 

STACIV: stato civile 
Stato civile del rispondente STACIV
> Celibe/nubile 1
> Convivente 2
> Sposato/sposata 3
> Vedovo/vedova 4
> Separato/separata 5
> Divorziato/Divorziata 6

!!!! PRIMA DI ATTIVARE FLASK !!!!

1. Far partire docker 

# Per runnare DOCKER 
nella cmd (con venv già attivata) scrivere:  docker-compose up -d 
il -d sta per detached, è possibile farlo partire anche senza  

# per bloccare DOCKER 
docker-compose stop 

# per bloccarlo definitivamente 
docker-compose down 

2. Nel file training-classifier seguire le istruzioni e runnare i 4 modelli (si salvaranno nella RAM) 

3. Dopo aver fatto runnare tutti e 4 i modelli, attivare flask nel solito modo  
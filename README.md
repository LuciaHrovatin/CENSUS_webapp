# BDT-Project
Big Data Technologies project


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



# Per runnare DOCKER 
nella cmd (con venv già attivata scrivere) 

docker-compose up -d (dove -d sta per detached) 

# per bloccare DOCKER 
docker-compose stop 

# per bloccarlo definitivamente 
docker-compose down 

# Solo dopo aver attivato docker runnare flask :) 
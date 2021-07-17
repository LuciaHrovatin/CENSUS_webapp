# C.E.N.S.U.S 
## *Calculator of Earnings Nationally Scored via User Specifics*
___

The C.E.N.S.U.S. project has been developed as final assignment of the Big Data Technologies course, offered by the University of Trento. 

## Project objective 
The project objective refers to deploying a web application, taking as input specific user data and returning a prediction of his/her income group, subcategorizing the Irpef system of taxation and its income segmentation. The prediction corresponds to the output of a Random Forest model trained with data provided by the Banca d’Italia and by the Sole24ore.
Specifically, the datasets employed are: 

- Banca d'Italia, Indagine sui bilanci delle famiglie italiane, [Indagine sul 2016](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/ricerca/ricerca.html?min_anno_pubblicazione=2018&max_anno_pubblicazione=2018) whose data refers to the 2016 survey 

- Banca d'Italia, Indagine sui bilanci delle famiglie italiane, [Indagine sul 2014](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/ricerca/ricerca.html?min_anno_pubblicazione=2015&max_anno_pubblicazione=2015) with data referring to the survey of 2014

- Lab24: [Qualità della vita](https://lab24.ilsole24ore.com/qualita-della-vita/) 

Whereas the Banca d’Italia offered a large amount of data per survey, only three datasets have been retained: **carcom**, containing the generalties of people who taken part into the survey, **rper**, individual income, and **rfam**, income per household. The variable descriptions, along with the survey items, can be found in the [Documentazione per l’utilizzo dei microdati](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/documentazione/index.html).             

## Prerequisites 

In order to run this project, the following tools have been installed on your workstation: 
- Python, preferably [3.9](https://www.python.org/downloads/release/python-390/) 
- [Docker Desktop](https://www.docker.com/), preferably 3.5
- [Docker Compose](https://docs.docker.com/compose/install/) v1.27.0 and newer

Older versions of `docker-compose` do not support all features required by the `docker-compose.yml` file, so check that the minimum version requirements are satisied.

## Installation 

### Clone the repository 

Clone this repository to a local directory typing in the command line: 

 ```
$  git clone https://github.com/elypaolazz/BDT-Project.git
```

### Environment 
The creation of a virtual environment is highly suggested. It can be created tipying in the command line (inside the project folder): 

```
virtualenv venv
```

The command above created a virtual environment named *venv*, which can be activated as follow.  

- in Unix systems:
    ```
    source venv
    ```

- in Windows systems:
    ```
    venv\Scripts\activate
    ```
### Requirements 

In the running virtual environment, install all libraries contained in the `requirements.txt` file:

```
pip install -r requirements.txt

```

## Usage

This project employs few Docker images: 
-	the official [apache-airflow Docker](https://hub.docker.com/r/apache/airflow) image with a Celery Executor and using the official [Postgres](https://hub.docker.com/_/postgres/) as backend and [Redis](https://hub.docker.com/_/redis/) as message broker.
 
-	the official [mysql](https://hub.docker.com/_/mysql) along with its web interface [phpmyadmit](https://hub.docker.com/_/phpmyadmin). 

-	the Docker image [shaynativ/redis-ml](https://hub.docker.com/r/shaynativ/redis-ml) that contains both the Redis server and the Redis ML module, used during the Machine Learning procedure. 

If running on **Linux** system, a further check for deploying Airflow is needed. The mounted volumes (in the `docker-compose.yml` file) use the user/group permissions, therefore double-check if the container and the host computer have matching file permissions.
```
mkdir ./dags  ./logs 
echo -e „AIRFLOW_UID=$(id -u) \nAIRFLOW_GID=0” > .env
```

### Activate Docker images 

On **all operating systems**, initialize the project running:
```
docker-compose up airflow-init  
```
The command above starts the database migrations and creates the Airflow user account passing as `username: airflow` and `password: airflow`. The initialization is complete when the message below appears:

```diff
# airflow-init_1   | Admin user airflow created 
# airflow-init_1   | 2.1.1
+ airflow-init_1 exited with code 0
```
Now is possible to start all the other services by typing:
```
docker-compose up 
```
If a detached mode is preferred: 
```
docker-compose up -d 
```
Furthermore, the logs are recalled with:
```
docker-compose logs [OPTIONAL: container name] 
```
**NOTE**:
The two-step procedure can be sidestepped by running the `docker-compose up -d` command only once. However, this shortcut implies a constant check of the containers' condition to detect when `airflow-init` exits:

```
docker-compose ps  

```
Specificaly, the resulting view should be the same as the screenshot below. 

--> immagine da inserire 

### Run the script 
After the virtual environment and the Docker images are set up, a last step must be manually performed. To start the entire data pipeline, type in the command line (within the virtual environment): 

```
python runner.py 
```

The pipeline will start following some steps: 
-	**ingestion phase**: the [requests](https://pypi.org/project/requests/) library data is downloaded from the Banca d’Italia and the Sole24ore websites 
-	**ETL phase**: a DAG in Airflow extracts relevant data, transforms it employing [pandas]( https://pandas.pydata.org/) Python library, and loads it to MySQL database `project_bdt`
-	**storage phase**: data is stored in a MySQL server running in another container 
-	**machine learning**: data is processed using Redis ML module implementing a [Random Forest model](https://redislabs.com/blog/introduction-redis-ml-part-five/) 
-	**web application**: the web application is launched and can be visited by clicking or copy-pasting the link in the terminal 



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

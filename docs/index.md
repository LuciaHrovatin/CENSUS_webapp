# CENSUS 
## *Calculator of Earnings Nationally Scored via User Specifics*
___

The CENSUS project has been developed as final assignment of the Big Data Technologies course, offered by the University of Trento. 

## Project objective 
The project objective refers to deploying a Big Data system, taking as input specific user data and returning a prediction of his/her income group, subcategorising the IRPEF system of taxation and its income segmentation. The prediction corresponds to the output of a Random Forest model trained with data provided by the Banca d’Italia and by the Sole24ore.
Specifically, the datasets employed are: 

- Banca d'Italia, Indagine sui bilanci delle famiglie italiane, [Indagine sul 2016](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/ricerca/ricerca.html?min_anno_pubblicazione=2018&max_anno_pubblicazione=2018) (published in 2018) whose data refers to the 2016 survey 

- Banca d'Italia, Indagine sui bilanci delle famiglie italiane, [Indagine sul 2014](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/ricerca/ricerca.html?min_anno_pubblicazione=2015&max_anno_pubblicazione=2015) (published in 2015) with data referring to the survey of 2014

- Sole24ore, Lab24: [Qualità della vita](https://lab24.ilsole24ore.com/qualita-della-vita/) 

Whereas the Banca d’Italia offers a large amount of data per survey, only three datasets are retained: **carcom**, containing the generalties of people who taken part into the survey, **rper**, individual income, and **rfam**, income per household. The variable descriptions, along with the survey items, can be found in the [Documentazione per l’utilizzo dei microdati](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/documentazione/index.html) and in `exploratory_data_analysis.Rmd`.             

## Prerequisites 

In order to run this project, the following tools have to be installed on your machine: 
- Python, preferably [3.9](https://www.python.org/downloads/release/python-390/) 
- [Docker Desktop](https://www.docker.com/), preferably 3.5
- [Docker Compose](https://docs.docker.com/compose/install/) v1.27.0 or newer

Older versions of `docker-compose` do not support all features required by the `docker-compose.yml` file, so check that the minimum version requirements are satisfied.

## Installation 

### Clone the repository 

Clone this repository in a local directory typing in the command line: 

```
git clone https://github.com/elypaolazz/BDT-Project.git
```

### Environment 
The creation of a virtual environment is highly suggested. If not already installed, install virtualenv:

- in Unix systems:
    ```
    python3 -m pip install --user virtualenv
    ```

- in Windows systems:
    ```
    python -m pip install --user virtualenv
    ```

And then create the virtual environment named *venv* typing in the command line (inside the project folder): 

- in Unix systems:
    ```
    python3 -m venv venv
    ```

- in Windows systems:
    ```
    python -m venv venv
    ```

The virtual environment can be activated as follow: 

- in Unix systems:
    ```
    source venv
    ```

- in Windows systems:
    ```
    venv\Scripts\activate
    ```
### Requirements 

In the active virtual environment, install all libraries contained in the `requirements.txt` file:

```
pip install -r requirements.txt
```

## Usage

This project employs few Docker images: 
-	the official [Apache-Airflow Docker](https://hub.docker.com/r/apache/airflow) image with Celery Executor, [PostgreSQL](https://hub.docker.com/_/postgres/) image as backend and [Redis](https://hub.docker.com/_/redis/) image as message broker.
 
-	the official [MySQL](https://hub.docker.com/_/mysql) image with its web interface [phpMyAdmin](https://hub.docker.com/_/phpmyadmin). 

-	the Docker image [shaynativ/redis-ml](https://hub.docker.com/r/shaynativ/redis-ml) that contains both the Redis server and the RedisML module, used during the Machine Learning procedure. 

If running on **Linux** system, a further check for deploying Airflow is needed. The mounted volumes (in the `docker-compose.yml` file) use the user/group permissions, therefore double-check if the container and the host computer have matching file permissions.
```
mkdir ./dags  ./logs 
echo -e "AIRFLOW_UID=$(id -u) \nAIRFLOW_GID=0" > .env
```
Further information available here: [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)

### Activate Docker images 

On **all operating systems**, initialise the project by running:
```
docker-compose up airflow-init  
```
The command above starts the database migrations and creates the Airflow user account passing as `username: airflow` and `password: airflow`. The initialisation is complete when the message below appears:

```diff
# airflow-init_1   | Admin user airflow created 
# airflow-init_1   | 2.1.1
+ airflow-init_1 exited with code 0
```
Now it is possible to start all the other services by running:
```
docker-compose up 
```
Or if a detached mode is preferred: 
```
docker-compose up -d 
```
Furthermore, the logs can be are recalled with:
```
docker-compose logs [OPTIONAL: container name] 
```

**NOTE**:
The two-step procedure can be sidestepped by running the `docker-compose up -d` command once. However, this shortcut implies a constant check of the containers' condition to detect when `airflow-init` exits:

```
docker-compose ps  
```
The resulting view should be the same as the below. 


### Run the script 
After the virtual environment and the Docker images set up, a last step must be manually performed. To start the entire data pipeline, type in the command line (with the activated virtual environment): 

- in Unix systems:
    ```
    python3 runner.py
    ```

- in Windows systems:
    ```
    python runner.py
    ```

The pipeline will start and follow these steps: 
-	**ingestion phase**: the [requests](https://pypi.org/project/requests/) Python library downloads the data from the Banca d’Italia and Sole24ore websites 
-	**ETL phase**: a DAG in Airflow extracts relevant data, transforms it employing [Pandas]( https://pandas.pydata.org/) Python library, and loads it to the MySQL database `project_bdt`
-	**storage phase**: data is stored in a MySQL server running in another container 
-	**machine learning**: data is processed using RedisML module and its [Random Forest algorithm](https://redislabs.com/blog/introduction-redis-ml-part-five/)
-	**web application**: the CENSUS web application is launched and can be visualised by clicking or copy-pasting the localhost link (appering in the terminal) in the browser 
    

### Access to webservers 
Accessing each service's webserver is the recommended approach to monitor the pipeline development. The webservers can be accessed in the browser by navigating to: 

-	**Airflow** [http://localhost:8080](http://localhost:8080/) a first log-in may be necessary with the chosen credentials (the default credentials are `username: airflow` and `password: airflow`). 

-	**Flower** [http://localhost:5555](http://localhost:5555/) for monitoring the tasks assigned to the Celery worker.  

-	**phpMyAdmim** [http://localhost:8082](http://localhost:8082/), which handles the administration of MySQL. As above, a log-in is required using the credentials chosen in the `docker-compose.yml` file (the default credentials are `server: mysql`, `user: root`, and `password: password`). 

### Access to CENSUS web application 

A user can access the web application in two different ways: 

1. clicking on the localhost link returned at the end of the data pipeline 

2. connecting to the stable CENSUS web application, hosted on a third-party server: [http://elisapaolazzi.pythonanywhere.com/]( http://elisapaolazzi.pythonanywhere.com/) 

The web application, reported below, predicts the income bracket of the user, following the [IRPEF](https://www.informazionefiscale.it/Irpef-2021-aliquote-scaglioni-calcolo-novita) categories and further sub-groups.  
Accessing the web application, you will see this page:


## Close the project and clean up 
The script will automatically end with the deployment of the web application. However, notice that: 

1. the logs of the web application will be uploaded on the terminal.

2. a manual stop of Docker containers is needed.

To stop and remove the running containers: 

```
docker-compose down 
```

To completely cleaning up the environment (i.e., delete containers, delete volumes with database data and download images), run:

```
docker-compose down --volumes --rmi all
```


## Troubleshooting
When running the project, some errors may occur 😥. The most common errors, together with a possible resolution, are listed below: 
-	Docker daemon does not reply after the `docker-compose up` command: relevant information can be found at the following link: [Configure and troubleshoot the Docker daemon](https://docs.docker.com/config/daemon/)

-	Other common errors are directly linked to the requests sent to the [Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/DAGRun). In particular:

```
ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
```

or 

```
CONNECTION ERROR: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response',))
```
The target machine refused the connection with the client. In this framework, it may refer to the fact that the Airflow initialisation procedure has not ended yet. 
The suggestion is to check the Docker container status by typing `docker-compose ps` or `docker-compose [airflow-init] logs` in the command line and wait until `airflow-init` exits.       
<br>
```
ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host
```
It refers to an overload of requests. A straightforward solution consists of setting a longer interval into the function `sleep()` present at the line 25 of the `runner.py` file. It is set to 30 seconds, but this temporal interval may not be enough. 

- When launching the webservers, a 
```
500 Internal Server Error
```
may arise. This server error response code indicates that the server encountered an unexpected condition that prevented it from fulfilling the request. Just try to refresh the page or to relaunch the webserver. 
If this error appears when submitting a prediction request to the CENSUS application, either a bug in the deployed code is present or the Redis server disconnected (to check if this second option is applicable, type: `docker-compose [redis-ml] logs`).  



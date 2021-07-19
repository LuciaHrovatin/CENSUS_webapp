# CENSUS 
## *Calculator of Earnings Nationally Scored via User Specifics*
___

The CENSUS project has been developed as final assignment of the Big Data Technologies course, offered by the University of Trento. 

## Project objective 
The project objective refers to deploying a Big Data system, taking as input specific user data and returning a prediction of his/her income group, subcategorizing the IRPEF system of taxation and its income segmentation. The prediction corresponds to the output of a Random Forest model trained with data provided by the Banca d’Italia and by the Sole24ore.
Specifically, the datasets employed are: 

- Banca d'Italia, Indagine sui bilanci delle famiglie italiane, [Indagine sul 2016](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/ricerca/ricerca.html?min_anno_pubblicazione=2018&max_anno_pubblicazione=2018) whose data refers to the 2016 survey 

- Banca d'Italia, Indagine sui bilanci delle famiglie italiane, [Indagine sul 2014](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/ricerca/ricerca.html?min_anno_pubblicazione=2015&max_anno_pubblicazione=2015) with data referring to the survey of 2014

- Lab24: [Qualità della vita](https://lab24.ilsole24ore.com/qualita-della-vita/) 

Whereas the Banca d’Italia offered a large amount of data per survey, only three datasets have been retained: **carcom**, containing the generalties of people who taken part into the survey, **rper**, individual income, and **rfam**, income per household. The variable descriptions, along with the survey items, can be found in the [Documentazione per l’utilizzo dei microdati](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/documentazione/index.html).             

## Prerequisites 

In order to run this project, the following tools have been installed on your machine: 
- Python, preferably [3.9](https://www.python.org/downloads/release/python-390/) 
- [Docker Desktop](https://www.docker.com/), preferably 3.5
- [Docker Compose](https://docs.docker.com/compose/install/) v1.27.0 and newer

Older versions of `docker-compose` do not support all features required by the `docker-compose.yml` file, so check that the minimum version requirements are satisied.

## Installation 

### Clone the repository 

Clone this repository to a local directory typing in the command line: 

```
git clone https://github.com/elypaolazz/BDT-Project.git
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
 
-	the official [mysql](https://hub.docker.com/_/mysql) along with its web interface [phpmyadmin](https://hub.docker.com/_/phpmyadmin). 

-	the Docker image [shaynativ/redis-ml](https://hub.docker.com/r/shaynativ/redis-ml) that contains both the Redis server and the Redis ML module, used during the Machine Learning procedure. 

If running on **Linux** system, a further check for deploying Airflow is needed. The mounted volumes (in the `docker-compose.yml` file) use the user/group permissions, therefore double-check if the container and the host computer have matching file permissions.
```
mkdir ./dags  ./logs 
echo -e „AIRFLOW_UID=$(id -u) \nAIRFLOW_GID=0” > .env
```
Further information available here: [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)

### Activate Docker images 

On **all operating systems**, initialize the project running:
```
docker-compose up airflow-init  
```
The command above starts the database migrations and creates the Airflow user account passing as `username: airflow` and `password: airflow`. The initialisation is complete when the message below appears:

```diff
# airflow-init_1   | Admin user airflow created 
# airflow-init_1   | 2.1.1
+ airflow-init_1 exited with code 0
```
Now it is possible to start all the other services by typing:
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
The two-step procedure can be sidestepped by running the `docker-compose up -d` command only once. However, this shortcut implies a constant check of the containers' condition to detect when `airflow-init` exits:

```
docker-compose ps  
```
Specificaly, the resulting view should be the same as the screenshot below. 

![Docker container's condition](static/container_condition.png)


### Run the script 
After the virtual environment and the Docker images are set up, a last step must be manually performed. To start the entire data pipeline, type in the command line (with the activated virtual environment): 

```
python runner.py 
```

The pipeline will start following some steps: 
-	**ingestion phase**: the [requests](https://pypi.org/project/requests/) Python library downloads the data from the Banca d’Italia and Sole24ore websites 
-	**ETL phase**: a DAG in Airflow extracts relevant data, transforms it employing [pandas]( https://pandas.pydata.org/) Python library, and loads it to the MySQL database `project_bdt`
-	**storage phase**: data is stored in a MySQL server running in another container 
-	**machine learning**: data is processed using Redis ML module implementing a [Random Forest model](https://redislabs.com/blog/introduction-redis-ml-part-five/) 
-	**web application**: the CENSUS web application is launched and can be visualized by clicking or copy-pasting the localhost (which will apperas in the terminal) link in the browser 
    

### Access to web servers 
Accessing each service web server is the recommended approach to monitor the pipeline development. The web servers can be accessed in the browser by navigating to: 

-	**Airflow** [http://localhost:8080](http://localhost:8080/) a first log-in may be necessary with the chosen credentials (the default credentials are `username: airflow` and `password: airflow`). 


![Airflow](static/airflow_2.png)


-	**Flower** [http://localhost:5555](http://localhost:5555/) for monitoring the tasks assigned to the Celery worker.  

-	**phpMyAdmit** [http://localhost:8082](http://localhost:8082/), which handles the administration of MySQL. Also in this case, a log-in is required reporting the credentials chosen in the `docker-compose.yml`file (the default credentials are `server: mysql`, `user: root`, and `password: password`). 

![phpMyAdmit](static/php.png)

### Access to CENSUS web application 

A user can access the web application in two different ways: 

1. clicking on the lochalhost link returned at the end of the data pipeline 

2. connecting to the stable CENSUS web application, hosted on a third-party server: [http://elisapaolazzi.pythonanywhere.com/]( http://elisapaolazzi.pythonanywhere.com/) 

The web application, reported below, predicts the income bracket of the user, following the [IRPEF](https://www.informazionefiscale.it/Irpef-2021-aliquote-scaglioni-calcolo-novita) categories and further sub-groups.  
Accessing to the web application, you will see this page:

![INTERFACE](static/interface.png)

## Close the project 
The script will automatically end with the deployment of the web application. However, a manual stop of the Docker containers is needed using the command: 

```
docker-compose down 
```
# Code structure

The backend code structure is composed by:
-   `airflow` folder, containing the dags files of the first three stages of the datapipeline: ingestion phase (`first_dag.py`), ETL phase (`second_dag.py`) and MySQL storage (`third_dag.py`)
-   `R_graph_scripts` folder, containing the R scripts for the interface plots  
-   `src`, containing Python files with specific functions for data collection, data transformation and machine learning training/testing process 
-   `docker-compose.yml`, docker file that defines the docker containers and their relationships  
-   `runner.py`, that triggers the entire project 

## Interface code structure
The system interface is a Flask web application composed by:
-   `main.py`, python file containing the function needed to launch the application in the local server and the route functions (that define variables, actions and events) of the different pages 
-   `forms.py`, file that defines and manages the application forms and their fields
-   `templates folder`, containing the HTML files for each page template
-   `static folder`, containing the CSS file for the presentation (layout, colors, and fonts) and the images

## Overall code structure
```
├── airflow
│   └── dags
│   	  ├── first_dag.py
│   	  ├── second_dag.py
│   	  └── third_dag.py
│
├── R_graph_scripts
│   ├── internet_map_graph.Rmd
│   ├── prezzo_abitaz_map_graph.Rmd
│	├── spazio_abitazz_map_graph.Rmd
│   └── spesa_fam_map_graph.Rmd
│ 
├── src
│   ├── classifier.py
│   ├── collector.py
│	├── province_ita.json
│   └── saver.py
│ 
├── static
│    ├── main.css
│    ├── graph.png
│    └── ...
│
├── templates
│    ├── about.htm
│    ├── home.htm
│    ├── layout.htm
│    └── line_chart.htm
│
├── .gitignore
├── docker-compose.yml
├── forms.py
├── main.py
├── requirements.txt
└── runner.py
```

## Troubleshooting
When running the project, some errors may occur. The most common together with an option for a possible resolution are listed below: 
-	Docker daemon does not reply after the docker-compose up command: relevant information can be found at the following link: [Configure and troubleshoot the Docker daemon](https://docs.docker.com/config/daemon/)

-	Other common errors are directly linked to the requests sent to the [Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/DAGRun). In particular:

```
ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
```
The target machine refused the connection with the client. In this framework, it may refer to the fact that the Airflow initialisation procedure has not ended yet. The suggestion is to check the Docker container status by typing `docker-compose ps` or `docker-compose [airflow-init] logs` in the command line and wait until airflow-init exits.       

```
ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host
```
It refers to an overload of requests. A straightforward solution consists of setting a longer interval into the function `sleep()` present at the line 25 of the `runner.py` file. It is set to 30 seconds, but this temporal interval may not be enough. 

- When launching the webservers, a 
```
500 Internal Server Error
```
may arise. This server error response code indicates that the server encountered an unexpected condition that prevented it from fulfilling the request. Just try to refresh the page or to relaunch the web server. If this error appears when submitting a prediction request to the CENSUS application, either a bug in the deployed code is present or the Redis server is disconnected (to check if this second option is applicable, type: `docker-compose [redis-ml] logs`).  



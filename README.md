# Airflow App Usage

## Description
This project uses an Apache Airflow pipeline which generates dummy .json data for a user's daily app usage and then adds that data to the Neo4j Graph Database.  
The first time the pipeline runs, it initially populates data for the last 30 days and as long as the scheduler is running, it will run every single day at midnight to populate the previous day's data.  

## Visuals

Airflow Webserver  
![Image1](https://github.com/Murtaza-Ali-2990/Airflow_App_Usage/blob/master/assets/Screenshot%202021-06-26%20002008.png?raw=true)  

Neo4j Graph Database
![Image2](https://github.com/Murtaza-Ali-2990/Airflow_App_Usage/blob/master/assets/Screenshot%202021-06-26%20002530.png?raw=true)  

![Image3](https://github.com/Murtaza-Ali-2990/Airflow_App_Usage/blob/master/assets/Screenshot%202021-06-26%20002635.png?raw=true)  

![Image4](https://github.com/Murtaza-Ali-2990/Airflow_App_Usage/blob/master/assets/Screenshot%202021-06-26%20003731.png?raw=true)  

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install airflow and neo4j database, as well as it's required divers. Refer to the following pages.  
[Installing Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html)  
[Installing Neo4j](https://debian.neo4j.com/?_ga=2.168396577.1483818822.1624525958-1761798042.1624367063)  
[Installing Neo4j Bolt driver for Python](https://pypi.org/project/neo4j/4.3.1/)  


I have installed these in Linux environment, please refer to the above guide for other environments.  

Clone the project in your repository.  

## Usage

Set the database credentials in the "app_usage_pipeline" DAG before running the pipeline. Save the code.

Assuming that you are in your present working directory, start your airflow webserver.    

```bash
export AIRFLOW_HOME=$(pwd)
airflow webserver --port 8080
```
Start your airflow scheduler to schedule the tasks.  

```bash
export AIRFLOW_HOME=$(pwd)
airflow scheduler
```
Run the Neo4j database.
```bash
sudo neo4j start
```
Just in case, if you change the code or the changes in DAG do not appear on the webserver, reset the airflow db and run the webserver again.

```bash
airflow db reset
```

Enabling the "app_usage_pipeline" dag and running it will generate JSON files of the format USERDATA-YYYY-MM-DD in the "userdata" directory.  

These files will then be uploaded by a PythonOperator using a Python Script into the Neo4j database.  

You can see these values in the Neo4j browser client.
```console
neo4j$: MATCH (n) RETURN n
```

## License
Airflow Community Version  
Neo4j Community Version  

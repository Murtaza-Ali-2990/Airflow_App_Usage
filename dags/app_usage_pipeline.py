from data_generation import app_usage_generation as usage
from neo4j_db_service import neo4j_database_service as dbservice

from datetime import datetime, timedelta
import os
import json

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Default arguments for every DAG in this file
default_args = {
    'owner': 'airflow',    
    'start_date': days_ago(30),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Directed Acyclic Graph (DAG) which directs the workflow of the pipeline
with DAG(
    dag_id = 'app_usage_generation',
    default_args= default_args,
    schedule_interval= '@daily',
    catchup= True,
) as dag:

    # Function which generates userdata .json file in "userdata" directory
    def generate_data(yesterday: str):
        
        day_format = '%Y-%m-%d'
        yesterday = (datetime.strptime(yesterday, day_format) - timedelta(days = 1)).strftime(day_format)

        # filepath is where we save the "userdata" directory
        filepath = os.path.abspath(os.getcwd())
        usage.generate_user_data(yesterday, filepath)

    # Task which will generate the .json file
    usage_data_generation_task = PythonOperator(
        task_id = 'data_gen_task',
        python_callable = generate_data,
        op_args = ['{{ ds }}'],
        dag = dag
    )

    # Function which will load data into the database
    def load_data(yesterday: str):

        day_format = '%Y-%m-%d'
        yesterday = (datetime.strptime(yesterday, day_format) - timedelta(days = 1)).strftime(day_format)

        # filepath is the path to the user app data
        filepath = os.path.abspath(os.getcwd()) + '/userdata/USERDATA-' + yesterday + '.json'
        with open(filepath, 'r') as fp:
            user_data = json.load(fp)

        # Start the Neo4j server before running this function
        bolt_url = "neo4j://localhost:7687"
        user = "neo4j"
        password = "neo4j"
        dbservice.app_usage_database_service(bolt_url, user, password, user_data)

    # Task which will upload the .json data to Neo4j database
    upload_to_database_task = PythonOperator(
        task_id = 'data_upload_task',
        python_callable = load_data,
        op_args = ['{{ ds }}'],
        dag = dag
    )

    # Directing the flow of task
    usage_data_generation_task >> upload_to_database_task

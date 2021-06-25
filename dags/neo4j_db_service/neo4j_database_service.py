from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

from datetime import datetime

class DatabaseService:

    def __init__(self, uri, user, password):
        # Connecting to the Neo4j database
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Closing the driver connection when we are finished with it.
        self.driver.close()

    # Function to create record in database
    def create_app_usage_record(self, app_usage: dict):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_app_usage_record, app_usage)
            if result == True:
                print("App usage record created for user {user}".format(user = app_usage['user_id']))

    # Function which runs a query and returns a result
    @staticmethod
    def _create_app_usage_record(tx, app_usage: dict):
        
        query = ("MERGE (user:User { IdMaster: $user_id }) ")
        result = tx.run(query, user_id = app_usage['user_id'])

        for app in app_usage['usages']:
            query = (
                "MATCH (user:User) WHERE user.IdMaster = $user_id "
                "CREATE (app:App { IdMaster: $app_name , AppCategory: $app_category }) "
                "CREATE (user)-[used:USED { TimeCreated: $time_created , TimeEvent: $usages_date , UsageMinutes: $minutes_used }]->(app) "
                "CREATE (device:Device { IdMaster: $device_os }) "
                "CREATE (app)-[on:ON { TimeCreated: $time_created }]->(device) "
                "CREATE (brand:Brand { IdMaster: $device_brand }) "
                "CREATE (device)-[of:OF { TimeCreated: $time_created }]->(brand) "
            )
            result = tx.run(query, 
                            user_id = app_usage['user_id'], 
                            app_name = app['app_name'],
                            app_category = app['app_category'],
                            time_created = datetime.now().isoformat(),
                            usages_date = app_usage['usages_date'],
                            minutes_used = app['minutes_used'],
                            device_os = app_usage['device']['os'],
                            device_brand = app_usage['device']['brand']
            )
        try:
            return True
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

def app_usage_database_service(bolt_url: str, user: str, password: str, app_usage_data: list):
    
    databaseService = DatabaseService(bolt_url, user, password)
    
    for user_app_usage_data in app_usage_data:
        databaseService.create_app_usage_record(user_app_usage_data)
    
    databaseService.close()

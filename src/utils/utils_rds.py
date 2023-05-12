import boto3

class RDSManager:

    def __init__(self, rds_client):
        self.rds_client = boto3.client('rds')

    def create_instance(
        self, db_name, db_instance_id, db_engine,
        db_instance_class, admin_name, admin_password):
        """
        Description: Creates a DB instance
        :param db_name: The name of the database that is created in the DB instance.
        :param instance_id: The ID to give the newly created DB instance.
        :param db_engine: The database engine of a database to create in the DB instance.
        :param instance_class: The DB instance class for the newly created DB instance.
        :param admin_name: The name of the admin user for the created database.
        :param admin_password: The admin password for the created database.
        :return: Data about the newly created DB instance.
        """
        try:
            response = self.rds_client.create_db_instance(
                DBName=db_name,
                DBInstanceIdentifier = db_instance_id,
                Engine = db_engine,
                DBInstanceClass = db_instance_class,
                MasterUsername=admin_name,
                MasterUserPassword=admin_password)
            db_inst = response['DBInstance']
        except Exception as e:
            print("Couldn't create DB instance")
            raise
        else:
            return db_inst
    
    def delete_instance(self, instance_id):
        """
        Description: Deletes a DB instance.
        :param instance_id: The ID of the DB instance to delete.
        :return: Data about the deleted DB instance.
        """
        try:
            response = self.rds_client.delete_db_instance(
                DBInstanceIdentifier=instance_id, SkipFinalSnapshot=True,
                DeleteAutomatedBackups=True)
            db_inst = response['DBInstance']
        except Exception as err:
            print("Couldn't delete DB instance")
            raise
        else:
            return db_inst
        
    def list_instance(self):
        """
        Description: Gets name off all DB instance.
        :param : None
        :return: Lista of all instance names.
        """
        try:
            response = self.rds_client.describe_db_instances()
            db_instance = []
            for instance in response['DBInstances']:
                db_instance.append(instance['DBInstanceIdentifier'])
        except Exception as e:
            print('Não foi possível verificar as instâncias')
            raise
        else:
            return db_instance


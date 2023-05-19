import boto3
from botocore.exceptions import ClientError

class RDSManager:

    def __init__(self):
        self.rds_client = boto3.Session(profile_name='default').client('rds')

    def generate_token(self, host, port, username, region):
        """
        Description: Generate token used to connect instance RDS
        :param : Host instance RDS, port , username , region AWS
        :return: token
        """
        return self.rds_client.generate_db_auth_token(DBHostname=host, Port=port, DBUsername=username, Region=region)

    def check_instance_exists(self, rds_instance_id):
        """
        Description: Check if instance exists
        :param : DB Instance ID
        :return: True ou False
        """
        try:
            response = self.rds_client.describe_db_instances(DBInstanceIdentifier=rds_instance_id)
            if response['DBInstances']:
                return response['DBInstances'][0]
        except ClientError as error_client:
            return None
        except Exception as e:
            raise
        else:
            return None

    def create_instance(self, db_name, rds_instance_id, db_engine,
        db_instance_class, admin_name, admin_password, port, vpc_security_group_id, subnet_name, public_access):
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
        if self.check_instance_exists(rds_instance_id):
            print('Instancia já existe')
            return self.check_instance_exists(rds_instance_id)
        else:
            try:
                response = self.rds_client.create_db_instance(
                    AllocatedStorage=10,
                    DBName=db_name,
                    DBInstanceIdentifier = rds_instance_id,
                    Engine = db_engine,
                    DBInstanceClass = db_instance_class,
                    MasterUsername=admin_name,
                    MasterUserPassword=admin_password,
                    Port=port,
                    VpcSecurityGroupIds=vpc_security_group_id,
                    DBSubnetGroupName = subnet_name,
                    PubliclyAccessible=public_access
                    )
                print('Instancia criada')
                self.rds_client.get_waiter('db_instance_available').wait(DBInstanceIdentifier=rds_instance_id)
                return response['DBInstance']
            except Exception as e:
                print("Não foi possível criar a instância do RDS")
                raise

    def get_rds_endpoint(self, rds_instance_id):
        try:
            response = self.rds_client.describe_db_instances(
                        DBInstanceIdentifier=rds_instance_id)
            endpoint = response.get('DBInstances')[0].get('Endpoint').get('Address')
            return endpoint
        except Exception as e:
            raise
    
    def delete_instance(self, instance_id):
        """
        Description: Delete a DB instance.
        :param instance_id: The ID of the DB instance to delete.
        :return: Data about the deleted DB instance.
        """
        try:
            response = self.rds_client.delete_db_instance(
                DBInstanceIdentifier=instance_id, SkipFinalSnapshot=True,
                DeleteAutomatedBackups=True)
            db_inst = response['DBInstance']
        except Exception as err:
            print("Não foi possível deletar a instância")
            raise
        else:
            return db_inst
        
    def list_all_instance(self):
        """
        Description: Gets name off all DB instances.
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
        
    def check_subnet_group_exists(self, subnet_group_name):
        """
        Description: Check subnet group exists
        :param : Name of subnet group
        :return: subnet group name.
        """
        try:
            response = self.rds_client.describe_db_subnet_groups(
                            DBSubnetGroupName=subnet_group_name,
                    )
        
            if response['DBSubnetGroups'][0]['DBSubnetGroupName'] == subnet_group_name:
                print(response['DBSubnetGroups'][0]['DBSubnetGroupName'])
                return response['DBSubnetGroups'][0]['DBSubnetGroupName']
            else:
                return None
            
        except self.rds_client.exceptions.DBSubnetGroupAlreadyExistsFault as e:
            return subnet_group_name
        except self.rds_client.exceptions.DBSubnetGroupNotFoundFault as er:
            return None


    def create_subnet_group(self, subnet_group_name, subnet_id1, subnet_id2):
        """
        Description: Check subnet group exists
        :param : Name of subnet group
        :return: subnet group name.
        """
        if self.check_subnet_group_exists(subnet_group_name):
            return self.check_subnet_group_exists(subnet_group_name)
        else:
            response = self.rds_client.create_db_subnet_group(
                                DBSubnetGroupName=subnet_group_name,
                                DBSubnetGroupDescription='RDS test',
                                SubnetIds=[
                                        subnet_id1,
                                        subnet_id2,
                                            ],
                                        )

            subnet_group_name = response['DBSubnetGroup']['DBSubnetGroupName']
            return subnet_group_name


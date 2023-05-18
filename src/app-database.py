from src.utils.utils_rds import RDSManager
from src.utils.utils_database import DatabaseConnector
from src.utils.utils_ec2 import EC2Manager
import configparser

cfg = configparser.ConfigParser()
cfg.read('D:\\projetos_python\\app_aws\\venv-app-aws\\src\\configaws.ini')
cfg.sections()

port = cfg.getint('RDS','port')
username = cfg['RDS']['username']
password = cfg['RDS']['password']
region = cfg['RDS']['region']
public_access = cfg.getboolean('RDS','public_access')
db_name = cfg['RDS']['db_name']
db_instance_id = cfg['RDS']['db_instance_id']
db_engine = cfg['RDS']['db_engine']
db_instance_class = cfg['RDS']['db_instance_class']

#[ec2]
vpc_cidr = cfg['EC2']['vpc_cidr']
subnet_cidr1 = cfg['EC2']['subnet_cidr1']
subnet_cidr2 = cfg['EC2']['subnet_cidr2']
region1 = cfg['EC2']['region1']
region2 = cfg['EC2']['region2']
vpc_name = cfg['EC2']['vpc_name']
subnet_name1 = cfg['EC2']['subnet_name1']
subnet_name2 = cfg['EC2']['subnet_name2']
#subnet_names = cfg['EC2']['subnet_names']
#print(subnet_names)
subnet_group_name = cfg['EC2']['subnet_group_name']
security_group_name = cfg['EC2']['security_group_name']
internet_gateway_name = cfg['EC2']['internet_gateway_name']
min_count = cfg.getint('EC2', 'min_count')
max_count = cfg.getint('EC2', 'max_count')
instance_type = cfg['EC2']['instance_type']

print(region1)
print(type(region1))

if __name__ == '__main__':

    rds_manager = RDSManager()
    ec2_manager = EC2Manager()

    # Cria uma instancia do EC2
    #instance_ec2 = ec2_manager.create_instance(ami, min_count, max_count, instance_type)
    vpc_security_group_id, subnet1, subnet2 = ec2_manager.create_all_resources_ec2(vpc_cidr, vpc_name,
                                                                                    subnet_cidr1, 
                                                                                    subnet_cidr2, 
                                                                                    subnet_name1, 
                                                                                    subnet_name2, 
                                                                                    region1, region2, 
                                                                                    security_group_name,
                                                                                    internet_gateway_name
                                                                                    )
    #Cria um subnet group no RDS
    subnet_group_name = rds_manager.create_subnet_group(subnet_group_name, subnet1, subnet2)

    rds_manager.create_instance(
        db_name, 
        db_instance_id, 
        db_engine, 
        db_instance_class, 
        username, 
        password,
        port,
        vpc_security_group_id,
        subnet_group_name,
        public_access
        )
    #Busca o host para conectar no RDS
    host = rds_manager.get_rds_endpoint(db_instance_id)
    # Cria uma instância do DatabaseConnector
    database_manager = DatabaseConnector(host=host, port=port, username=username, password=password, db_name=db_name)
    # Cria um novo banco de dados
    database_manager.create_database(db_name)

    # Concede privilégios a um usuário no novo banco de dados
    #database_manager.grant_privileges(username, password, db_name)

    # Revoga privilégios do usuário no novo banco de dados
    #database_manager.revoke_privileges('new_user', 'new_db')

    # Deleta o banco de dados criado anteriormente
    #database_manager.delete_database('new_db')

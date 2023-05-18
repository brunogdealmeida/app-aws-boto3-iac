import boto3
import pymysql

class RDSConnector:

    def __init__(self, rds_host, username, password, db_name):
        self.rds_hot = rds_host
        self.username = username
        self.password = password
        self.db_name = db_name

    def connect(self, engine_db):
        engine = {
                'mysql':'pymysql.connect(self.rds_host, user=self.name, passwd=self.password, db=self.db_name, connect_timeout=5)'
                 }
        conn = engine[engine_db]
        return conn
    
    def execute_sql(self, sql):
        try:
            conn = self.connect()
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
            conn.close()
            return True
        except Exception as e:
            raise
        else:
            return False
        
    def select_sql(self, sql):
        try:
            conn = self.connect()
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            raise
        else:
            return None
        
    def create_database(self, db_name):
        """
        Creates a new database in the RDS instance
        """
        try:
            conn = pymysql.connect(
                host=self.rds_host, user=self.user, password=self.password, port=self.port)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {db_name}")
            conn.commit()
        except Exception as e:
            raise
        finally:
            conn.close()

    def delete_database(self, db_name):
        """
        Deletes a database from the RDS instance
        """
        try:
            conn = pymysql.connect(
                host=self.rds_host, user=self.user, password=self.password, port=self.port)
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE {db_name}")
            conn.commit()
        except Exception as e:
            raise
        finally:
            conn.close()

    def grant_privileges(self, username, password, db_name):
        """
        Grants privileges to a user on a specific database
        """
        try:
            conn = pymysql.connect(
                host=self.rds_host, user=self.user, password=self.password, port=self.port)
            cursor = conn.cursor()
            cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{username}'@'%' IDENTIFIED BY '{password}'")
            conn.commit()
        except Exception as e:
            print("Couldn't grant privileges")
            raise
        finally:
            conn.close()

    def revoke_privileges(self, username, db_name):
        """
        Revokes privileges from a user on a specific database
        """
        try:
            conn = pymysql.connect(
                host=self.rds_host, user=self.user, password=self.password, port=self.port)
            cursor = conn.cursor()
            cursor.execute(f"REVOKE ALL PRIVILEGES ON {db_name}.* FROM '{username}'@'%'")
            conn.commit()
        except Exception as e:
            print("Couldn't revoke privileges")
            raise
        finally:
            conn.close()

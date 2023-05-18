import boto3
import pymysql

class DatabaseConnector:

    def __init__(self, host, port, username, password, db_name):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name

    def _connect(self):
        """
        Intern method , connect to MySQL RDS
        :param : Username, password and DB name
        :return : True or False
        """
        conn = pymysql.connect(
                            host=self.host, 
                            user=self.username, 
                            password=self.password, 
                            connect_timeout=60
                            )
        return conn
    
    def create_database(self, new_database_name):
        """
        Creates a new database
        :param : New DB Name
        :return: database connection 
        """
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(f'''CREATE DATABASE IF NOT EXISTS {new_database_name}''')
                conn.commit()
        except Exception as e:
            raise
        else:
            conn.close()
            

    def delete_database(self, database_name):
        """
        Delete database
        :param : DB name
        :return : True or False 
        """
        try:
            with self._connect as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f'DROP DATABASE IF EXISTS {database_name}')
                    conn.commit()
            return True
        except Exception as e:
            raise
        else:
            return False
    
    def execute_query(self, sql_query):
        """
        Execute Query SQL
        :param : SQL Query (Update, Delete)
        :return : True or False
        """
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                conn.commit()
            conn.close()
            return True
        except Exception as e:
            raise
        else:
            return False
        
    def execute_query_select(self, sql_query_select):
        """
        Execute Query SQL
        :param : SQL Query (Select)
        :return : True or False
        """
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(sql_query_select)
                result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            raise
        finally:
            conn.close()

    def grant_privileges(self, username, password, db_name):
        """
        Grant privileges to user
        :param : Username, password and DB name
        :return : True or False
        """
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{username}'@'%' IDENTIFIED BY '{password}'")
                conn.commit()
            return True
        except Exception as e:
            print("Não foi possível dar acesso.")
            raise
        else: 
            return False

    def revoke_privileges(self, username, db_name):
        """
        Revokes privileges from a user on a specific database
        :param : Username, password and DB name
        :return : True or False
        """
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(f"REVOKE ALL PRIVILEGES ON {db_name}.* FROM '{username}'@'%'")
                conn.commit()
            return True
        except Exception as e:
            print("Não foi possível revogar os privilégios.")
            raise
        else:
            return False
        finally:
            conn.close()

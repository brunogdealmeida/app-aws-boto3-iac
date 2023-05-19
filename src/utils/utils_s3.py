import boto3

# To Do
# Uploading multiple files to S3 bucket
# Reading files from the S3 bucket into memory
# Creating S3 Bucket Policy using Boto3
# Deleting S3 Bucket Policy using Boto3
# Generating S3 presigned URL
# Enabling S3 Bucket versioning using Boto3

class S3Manager:

    def __init__(self, profile_name='default'):
        self.client = boto3.Session(profile_name='default').client('s3')

    def list_buckets(self):
        """
        List all buckets
        :param : Username, password and DB name
        :return : True or False
        """
        response = self.client.list_buckets()
        return [bucket['Name'] for bucket in response.get('Buckets', [])]

    def create_bucket(self, bucket_name, region=None):
        kwargs = {'Bucket': bucket_name}
        if region:
            kwargs['CreateBucketConfiguration'] = {'LocationConstraint': region}
        try:
            self.client.create_bucket(**kwargs)
            print(f"Bucket '{bucket_name}' criado com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao criar o bucket '{bucket_name}': {str(e)}")
            return False

    def delete_bucket(self, bucket_name):
        """
        Delete specific bucket
        :param : Bucket name
        :return : True or False
        """
        try:
            self.client.delete_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' deletado com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao deletar o bucket '{bucket_name}': {str(e)}")
            return False

    def list_files(self, bucket_name):
        """
        List all files in a bucket
        :param : Bucket name
        :return : List of all files in the informed bucket
        """
        response = self.client.list_objects_v2(Bucket=bucket_name)
        return [obj['Key'] for obj in response.get('Contents', [])]

    def list_folders(self, bucket_name):
        """
        List all folders in a buckets
        :param : Bucket name
        :return : List of folders
        """
        response = self.client.list_objects_v2(Bucket=bucket_name, Delimiter='/')
        return [folder['Prefix'] for folder in response.get('CommonPrefixes', [])]

    def create_folder(self, bucket_name, folder_name):
        """
        Create folder in a bucket
        :param : Bucket name , folder name
        :return : True or False
        """
        try:
            self.client.put_object(Bucket=bucket_name, Key=folder_name+'/')
            print(f"Folder '{folder_name}' criado com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao criar o folder '{folder_name}': {str(e)}")
            return False

    def delete_file(self, bucket_name, object_name):
        """
        Delete specific in a bucket
        :param : bucket name , file name
        :return : True or False
        """
        try:
            self.client.delete_object(Bucket=bucket_name, Key=object_name)
            print(f"Objeto '{object_name}' deletado do bucket '{bucket_name}'.")
            return True
        except Exception as e:
            print(f"Erro ao deletar o objeto '{object_name}' do bucket '{bucket_name}': {str(e)}")
            return False

    def delete_all_files(self, bucket_name):
        """
        Delete all files in a bucket
        :param : bucket name
        :return : True or False
        """
        try:
            response = self.client.list_object_versions(Bucket=bucket_name)
            if 'DeleteMarkers' in response:
                delete_markers = [{'VersionId': marker['VersionId'], 'Key': marker['Key']} for marker in response['DeleteMarkers']]
                self.client.delete_objects(Bucket=bucket_name, Delete={'Objects': delete_markers})
            if 'Versions' in response:
                versions = [{'VersionId': version['VersionId'], 'Key': version['Key']} for version in response['Versions']]
                self.client.delete_objects(Bucket=bucket_name, Delete={'Objects': versions})
            print(f"Todos os objetos do bucket '{bucket_name}' foram deletados.")
            return True
        except Exception as e:
            print(f"Erro ao deletar todos os objetos do bucket '{bucket_name}': {str(e)}")
            return False

    def download_file(self, bucket_name, file_name, download_path):
        """
        Donwload file from bucket
        :param :bucket name, file name , path destiny file
        :return : True or False
        """
        try:
            self.client.download_file(bucket_name, file_name, download_path)
            print(f"Objeto '{file_name}' do bucket '{bucket_name}' foi baixado com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao baixar o objeto '{file_name}' do bucket '{bucket_name}': {str(e)}")
            return False

    def upload_file(self, file_path, bucket_name, file_name):
        """
        Upload file to bucket
        :param : source file path, bucket name, file name
        :return : True or False
        """
        try:
            self.client.upload_fileobj(file_path, bucket_name, file_name)
            print('Upload realidado com sucesso.')
            return True
        except Exception as e:
            print('Erro no upload do arquivo.')
            raise

    def check_bucket_exists(self, bucket_name):
        """
        Check if specific bucket exists
        :param : bucket name
        :return : True or False
        """
        try:
            self.client.head_bucket(Bucket=bucket_name)
            return True
        except:
            return False
        
    def check_file_exists(self, bucket_name, filename):
        """
        Check if specific file exists in bucket
        :param : bucket name, filename
        :return : True or False
        """
        try: 
            files = self.client.list_objects_v2(Bucket=bucket_name)

            for file in files['Contents']:
                if file['Key'] == filename:
                    return True
                else:
                    return False    
        except Exception as e:
            raise

    def list_files_in_bucket(self, bucket_name):
        """
        List all files of a bucket
        :param : bucket name
        :return : True or False
        """
        try: 
            files = self.client.list_objects_v2(Bucket=bucket_name)
            list_files = []
            for file in files['Contents']:
                list_files.append(file['Key'])
            return list_files
        except Exception as e:
            raise

    def rename_file_bucket(self, bucket_name, old_filename, new_filename):
        """
        Rename file in bucket
        :param : bucket name
        :return : True or False
        """
        try:
            self.client.copy_object(Bucket=bucket_name,CopySource=f'{bucket_name}/{old_filename}',Key=new_filename)
            self.delete_file(bucket_name, old_filename)
            return True
        except Exception as e:
            raise

    
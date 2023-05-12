import pytest
from moto import mock_s3, mock_rds
from src.utils.utils_s3 import S3Manager
from src.utils.utils_rds import RDSManager
import io
import boto3


@pytest.fixture
def s3_manager():
    with mock_s3():
        s3 = S3Manager()
        yield s3

@pytest.fixture
def rds_manager():
    with mock_rds():
        rds_client = boto3.client('rds')
        rds_manager = RDSManager(rds_client)
        yield rds_manager

def test_create_bucket(s3_manager):
    assert s3_manager.create_bucket('my-bucket') == True

def test_list_buckets(s3_manager):
    s3_manager.create_bucket('my-bucket')
    assert s3_manager.list_buckets() == ['my-bucket']

def test_upload_file(s3_manager):
    file_path = f'D:\\projetos_python\\test.txt'
    s3_manager.create_bucket('my-bucket')
    file = io.BytesIO(b'Hello World')
    assert s3_manager.upload_file(file,'my-bucket','test.txt') == True

def test_download_file(s3_manager):
    s3_manager.create_bucket('my-bucket')
    s3_manager.upload_file(io.BytesIO(b'Hello World'), 'my-bucket', 'test.txt')
    assert s3_manager.download_file('my-bucket', 'test.txt', 'downloaded.txt') == True
    with open('downloaded.txt', 'r') as f:
        assert f.read() == 'Hello World'

def test_check_file_exists_in_bucket(s3_manager):
    s3_manager.create_bucket('my-bucket')
    s3_manager.upload_file(io.BytesIO(b'Hello World'), 'my-bucket', 'test.txt')
    assert s3_manager.check_file_exists('my-bucket','test.txt') == True

def test_list_files_in_bucket(s3_manager):
    s3_manager.create_bucket('my-bucket')
    file_hello_world = io.BytesIO(b'Hello World')
    s3_manager.upload_file(file_hello_world,'my-bucket','hello.txt')
    file_hi_there = io.BytesIO(b'Hi there')
    s3_manager.upload_file(file_hi_there,'my-bucket','hi.txt') == True
    assert s3_manager.list_files_in_bucket('my-bucket') == ['hello.txt','hi.txt']

def test_rename_file_bucket(s3_manager):
    s3_manager.create_bucket('my-bucket')
    file = io.BytesIO(b'Hello')
    s3_manager.upload_file(file, 'my-bucket', 'hello.txt')

def test_create_instance_rds(rds_manager):
    db_name = 'test_db'
    db_instance_id = 'test_db_instance'
    db_engine = 'mysql'
    db_instance_class = 'db.t2.micro'
    admin_name = 'admin'
    admin_password = 'password'

    db_instance = rds_manager.create_instance(
                            db_name, db_instance_id, db_engine,
                            db_instance_class, admin_name, admin_password
                                            )

    assert db_instance['DBInstanceIdentifier'] == db_instance_id

def test_delete_instance(rds_manager):
    db_name = 'test_db'
    db_instance_id = 'test_db_instance'
    db_engine = 'mysql'
    db_instance_class = 'db.t2.micro'
    admin_name = 'admin'
    admin_password = 'password'

    response = rds_manager.create_instance(
                            db_name, db_instance_id, db_engine,
                            db_instance_class, admin_name, admin_password
                                          )
    assert response['DBInstanceIdentifier'] == 'test_db_instance'

def test_list_instance(rds_manager):
    db_name = 'test_db'
    db_instance_id = 'test_db_instance'
    db_engine = 'mysql'
    db_instance_class = 'db.t2.micro'
    admin_name = 'admin'
    admin_password = 'password'

    rds_manager.create_instance(
                            db_name, db_instance_id, db_engine,
                            db_instance_class, admin_name, admin_password
                                        )
    assert rds_manager.list_instance() == ['test_db_instance']
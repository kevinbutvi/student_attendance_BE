import os
from dotenv import load_dotenv

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

INFLUX_URL = os.getenv('INFLUX_URL')
INFLUX_TOKEN = os.getenv('DOCKER_INFLUXDB_INIT_ADMIN_TOKEN')
INFLUX_ORG = os.getenv('DOCKER_INFLUXDB_INIT_ORG')
INFLUX_BUCKET = os.getenv('DOCKER_INFLUXDB_INIT_BUCKET')


class InfluxDBConn:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__init__(*args, **kwargs)

        return cls._instance

    def __init__(self, token=INFLUX_TOKEN, org=INFLUX_ORG, bucket=INFLUX_BUCKET, write_options=SYNCHRONOUS):
        self.token = token
        self.org = org
        self.bucket = bucket
        self.db_connection(write_options)

    def db_connection(self, write_options):
        self.__client = InfluxDBClient(
            url=INFLUX_URL, token=self.token, org=self.org)
        self.__query_api = self.__client.query_api()
        self.__write_api = self.__client.write_api(write_options)

    def read_query(self, query):
        results = self.__query_api.query(query)
        table_list = list(results)
        return table_list

    def write_data(self, data: list | Point, bucket=None, org=None):
        bucket = bucket or self.bucket
        org = org or self.org
        self.__write_api.write(bucket=bucket, org=org, record=data)

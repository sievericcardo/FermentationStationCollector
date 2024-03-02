from typing import Iterable, Optional, Union

from influxdb_client import Bucket, InfluxDBClient, Point
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS

from collector.config import CONFIG_PATH


class InfluxController:
    """
    Singleton class that handles the connection to InfluxDB.

    Attributes:
        __instance: the singleton instance
        __client: the InfluxDB client used to interact with the database
    """

    # https://influxdb-client.readthedocs.io/en/latest/
    __instance = None
    __client: InfluxDBClient = InfluxDBClient.from_config_file(CONFIG_PATH)

    def __new__(cls):
        """
        Create a new instance of the class if it does not exist, otherwise return the existing one
        """
        if cls.__instance is None:
            cls.__instance = super(InfluxController, cls).__new__(cls)

        return cls.__instance

    def delete_bucket(self, bucket_name: str) -> bool:
        """
        Delete a bucket from InfluxDB by name

        Attributes:
            bucket_name: the name of the bucket to delete

        Returns:
            True if the bucket was deleted, False otherwise
        """
        bucket = self.get_bucket(bucket_name)
        if bucket is None:
            return False

        self.__client.buckets_api().delete_bucket(bucket)
        return True

    def get_bucket(self, bucket_name: str) -> Optional[Bucket]:
        """
        Get a bucket from InfluxDB by name

        Attributes:
            bucket_name: the name of the bucket to get

        Returns:
            the bucket if it exists, None otherwise
        """
        return self.__client.buckets_api().find_bucket_by_name(bucket_name)

    def create_bucket(self, bucket_name: str) -> Bucket:
        """
        Create a new bucket in InfluxDB with name bucket_name if it does not exist, otherwise return the existing one

        Attributes:
            bucket_name: the name of the bucket to create

        Returns:
            the bucket
        """
        bucket = self.get_bucket(bucket_name)
        if bucket is not None:
            return bucket

        return self.__client.buckets_api().create_bucket(bucket_name=bucket_name)

    def write_point(self, point: Union[Point, Iterable[Point]], bucket: Bucket) -> bool:
        """
        Write a Point or Iterable of Points to bucket

        Attributes:
            point: the Point or Iterable of Points to write
            bucket: the bucket to write to

        Returns:
            True if the point was written, False otherwise
        """
        try:
            if (
                self.__client.write_api(write_options=SYNCHRONOUS).write(
                    bucket=bucket.name, org=self.__client.org, record=point
                )
                is None
            ):
                return True
            return False
        except InfluxDBError as e:
            print("Error while writing point in influxController.write_point: ", e)
            return False

    def close(self):
        self.__client.close()

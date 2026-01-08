import os

from config import index_settings
from elasticsearch import Elasticsearch
from temporalio import activity


class ElasticSearchClient:
    def __init__(self, index_name: str, host: str):
        if host is None:
            host = os.getenv("ELASTICSEARCH_ADDRESS", "http://localhost:9200")
        self._es = Elasticsearch(host)
        self.settings = index_settings
        self.index_name = index_name
        self.create_indices()

    @activity.defn
    def create_indices(self):
        if not self._es.indices.exists(index=self.index_name):
            self._es.indices.create(index=self.index_name, body=self.settings)
        else:
            print(f"Index {self.index_name} already exists")


if __name__ == "__main__":
    es = ElasticSearchClient(index_name="podcasts", host="http://localhost:9200")

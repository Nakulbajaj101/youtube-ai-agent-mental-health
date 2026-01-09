from config import (
    ELASTIC_SEARCH_API_KEY,
    ELASTIC_SEARCH_HOST,
    index_settings,
    INDEX_NAME,
)
from elasticsearch import Elasticsearch
from temporalio import activity


class ElasticSearchClient:
    def __init__(self, index_name: str):
        self._host = ELASTIC_SEARCH_HOST
        if ELASTIC_SEARCH_API_KEY:
            self.__key = ELASTIC_SEARCH_API_KEY
            self._client = Elasticsearch(hosts=self._host, api_key=self.__key)
        else:
            self._client = Elasticsearch(hosts=self._host)
        self.settings = index_settings
        self.index_name = index_name
        self.create_indices()

    @activity.defn
    def create_indices(self):
        if not self._client.indices.exists(index=self.index_name):
            self._client.indices.create(index=self.index_name, body=self.settings)
        else:
            print(f"Index {self.index_name} already exists")


if __name__ == "__main__":
    es = ElasticSearchClient(index_name=INDEX_NAME)

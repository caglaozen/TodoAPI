from elasticsearch import Elasticsearch

from src.config.elasticsearch_config import ELASTICSEARCH_HOST, ELASTICSEARCH_INDEX, ELASTICSEARCH_PORT


class ElasticsearchClient:
    def __init__(self):
        self.client = Elasticsearch([{"host": ELASTICSEARCH_HOST, "port": ELASTICSEARCH_PORT, "scheme": "http"}])

    def index_todo(self, todo: dict):
        self.client.index(index=ELASTICSEARCH_INDEX, id=todo["item_id"], document=todo)

    def search_todos(self, query: str):
        body = {"query": {"multi_match": {"query": query, "fields": ["title", "description"]}}}
        return self.client.search(index=ELASTICSEARCH_INDEX, body=body)

    def delete_todo(self, item_id: str):
        self.client.delete(index=ELASTICSEARCH_INDEX, id=item_id, ignore=[404])

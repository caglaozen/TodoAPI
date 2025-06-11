import os

ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST", "elasticsearch")
ELASTICSEARCH_PORT = int(os.environ.get("ELASTICSEARCH_PORT", 9200))
ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX", "todos")

import unittest
from unittest.mock import MagicMock, patch

from src.core.elasticsearch_client import ElasticsearchClient


class TestElasticsearchClient(unittest.TestCase):
    @patch("src.core.elasticsearch_client.Elasticsearch")
    def test_init(self, mock_es):
        """Test ElasticsearchClient initialization."""
        mock_client = MagicMock()
        mock_es.return_value = mock_client

        es_client = ElasticsearchClient()

        self.assertEqual(es_client.client, mock_client)
        mock_es.assert_called_once_with([{"host": "elasticsearch", "port": 9200, "scheme": "http"}])

    @patch("src.core.elasticsearch_client.Elasticsearch")
    def test_index_todo(self, mock_es):
        """Test indexing a todo in Elasticsearch."""
        mock_client = MagicMock()
        mock_es.return_value = mock_client

        es_client = ElasticsearchClient()
        todo = {"item_id": "123", "title": "Test Todo", "description": "Test Description"}

        es_client.index_todo(todo)

        mock_client.index.assert_called_once_with(index="todos", id="123", document=todo)

    @patch("src.core.elasticsearch_client.Elasticsearch")
    def test_search_todos(self, mock_es):
        """Test searching todos in Elasticsearch."""
        mock_client = MagicMock()
        mock_es.return_value = mock_client
        mock_client.search.return_value = {"hits": {"hits": []}}

        es_client = ElasticsearchClient()
        result = es_client.search_todos("test query")

        expected_body = {"query": {"multi_match": {"query": "test query", "fields": ["title", "description"]}}}
        mock_client.search.assert_called_once_with(index="todos", body=expected_body)
        self.assertEqual(result, {"hits": {"hits": []}})

    @patch("src.core.elasticsearch_client.Elasticsearch")
    def test_delete_todo(self, mock_es):
        """Test deleting a todo from Elasticsearch."""
        mock_client = MagicMock()
        mock_es.return_value = mock_client

        es_client = ElasticsearchClient()
        es_client.delete_todo("123")

        mock_client.delete.assert_called_once_with(index="todos", id="123", ignore=[404])

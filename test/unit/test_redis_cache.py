import json
import logging
import unittest
from unittest.mock import MagicMock, patch

import redis

from src.core.redis_cache import RedisCache

logging.disable(logging.CRITICAL)


class TestRedisCache(unittest.TestCase):
    @patch("src.core.redis_cache.redis.Redis")
    def test_init_successful_connection(self, mock_redis):
        """Test successful Redis connection initialization."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True

        cache = RedisCache()

        self.assertIsNotNone(cache.redis_client)
        mock_redis.assert_called_once_with(host="redis", port=6379)
        mock_client.ping.assert_called_once()

    @patch("src.core.redis_cache.redis.Redis")
    def test_init_connection_error(self, mock_redis):
        """Test Redis connection error handling."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.side_effect = redis.ConnectionError("Connection failed")

        cache = RedisCache()

        self.assertIsNone(cache.redis_client)

    @patch.dict("os.environ", {"REDIS_HOST": "custom-host", "REDIS_PORT": "6380"})
    @patch("src.core.redis_cache.redis.Redis")
    def test_init_with_custom_env_vars(self, mock_redis):
        """Test initialization with custom environment variables."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True

        RedisCache()

        mock_redis.assert_called_once_with(host="custom-host", port=6380)

    @patch("src.core.redis_cache.redis.Redis")
    def test_get_successful(self, mock_redis):
        """Test successful get operation."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True
        mock_client.get.return_value = json.dumps({"key": "value"})

        cache = RedisCache()
        result = cache.get("test_key")

        self.assertEqual(result, {"key": "value"})
        mock_client.get.assert_called_with("test_key")

    @patch("src.core.redis_cache.redis.Redis")
    def test_get_key_not_found(self, mock_redis):
        """Test get operation when key is not found."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True
        mock_client.get.return_value = None

        cache = RedisCache()
        result = cache.get("nonexistent_key")

        self.assertIsNone(result)

    @patch("src.core.redis_cache.redis.Redis")
    def test_get_with_no_redis_client(self, mock_redis):
        """Test get operation when Redis client is None."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.side_effect = redis.ConnectionError("Connection failed")

        cache = RedisCache()
        result = cache.get("test_key")

        self.assertIsNone(result)

    @patch("src.core.redis_cache.redis.Redis")
    def test_get_with_exception(self, mock_redis):
        """Test get operation handles exceptions."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True
        mock_client.get.side_effect = Exception("Redis error")

        cache = RedisCache()
        result = cache.get("test_key")

        self.assertIsNone(result)

    @patch("src.core.redis_cache.redis.Redis")
    def test_set_successful(self, mock_redis):
        """Test successful set operation."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True

        cache = RedisCache()
        cache.set("test_key", {"key": "value"})

        mock_client.set.assert_called_with("test_key", json.dumps({"key": "value"}))

    @patch("src.core.redis_cache.redis.Redis")
    def test_set_with_object(self, mock_redis):
        """Test set operation with object containing __dict__."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True

        class TestObject:
            def __init__(self):
                self.field = "value"

        cache = RedisCache()
        obj = TestObject()
        cache.set("test_key", obj)

        mock_client.set.assert_called_once()
        args, _ = mock_client.set.call_args
        self.assertEqual(args[0], "test_key")

    @patch("src.core.redis_cache.redis.Redis")
    def test_set_with_no_redis_client(self, mock_redis):
        """Test set operation when Redis client is None."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.side_effect = redis.ConnectionError("Connection failed")

        cache = RedisCache()
        cache.set("test_key", {"key": "value"})

        # No assertion needed - just verify it doesn't raise an exception

    @patch("src.core.redis_cache.redis.Redis")
    def test_set_with_exception(self, mock_redis):
        """Test set operation handles exceptions."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True
        mock_client.set.side_effect = Exception("Redis error")

        cache = RedisCache()
        cache.set("test_key", {"key": "value"})

        mock_client.set.assert_called_once()

    @patch("src.core.redis_cache.redis.Redis")
    def test_delete_successful(self, mock_redis):
        """Test successful delete operation."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True
        mock_client.delete.return_value = 1

        cache = RedisCache()
        result = cache.delete("test_key")

        self.assertTrue(result)
        mock_client.delete.assert_called_with("test_key")

    @patch("src.core.redis_cache.redis.Redis")
    def test_delete_key_not_found(self, mock_redis):
        """Test delete operation when key is not found."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True
        mock_client.delete.return_value = 0

        cache = RedisCache()
        result = cache.delete("nonexistent_key")

        self.assertFalse(result)

    @patch("src.core.redis_cache.redis.Redis")
    def test_delete_with_no_redis_client(self, mock_redis):
        """Test delete operation when Redis client is None."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.side_effect = redis.ConnectionError("Connection failed")

        cache = RedisCache()
        result = cache.delete("test_key")

        self.assertFalse(result)

    @patch("src.core.redis_cache.redis.Redis")
    def test_delete_with_exception(self, mock_redis):
        """Test delete operation handles exceptions."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True
        mock_client.delete.side_effect = Exception("Redis error")

        cache = RedisCache()
        result = cache.delete("test_key")

        self.assertFalse(result)

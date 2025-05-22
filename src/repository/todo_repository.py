from src.config.redis_config import ALL_TODOS_KEY, TODO_ITEM_KEY_PREFIX
from src.core.redis_cache import RedisCache
from src.model.todo_item import TodoItem


class TodoRepository:
    def __init__(self):
        """
        Initialize the TodoRepository with Redis cache only, without file storage.
        """
        self.cache = RedisCache()
        self.todos = self._load_from_redis()

    def add(self, todo):
        """
        Adds a new TodoItem to the repository in Redis.

        :param todo: The TodoItem instance to add.
        :raises ValueError: If a TodoItem with the same ID already exists.
        """
        if self.find_by_id(todo.item_id):
            raise ValueError(f"A TodoItem with ID {todo.item_id} already exists.")
        self.todos.append(todo)
        self._save_to_redis()
        self.cache.set(f"{TODO_ITEM_KEY_PREFIX}{todo.item_id}", todo)

    def find_by_id(self, item_id):
        """
        Finds a TodoItem by its ID in Redis.
        If found in cache, return it; otherwise search in repository list.
        """
        item_id_str = str(item_id)
        cached_todo = self.cache.get(f"{TODO_ITEM_KEY_PREFIX}{item_id_str}")
        if cached_todo:
            return TodoItem(**cached_todo) if isinstance(cached_todo, dict) else cached_todo

        for todo in self.todos:
            if str(todo.item_id) == item_id_str:
                self.cache.set(f"{TODO_ITEM_KEY_PREFIX}{todo.item_id}", todo)
                return todo

        return None

    def delete(self, item_id):
        """
        Deletes a TodoItem by its ID from Redis.

        :param item_id: The ID of the TodoItem to delete.
        """
        todo = self.find_by_id(item_id)
        if not todo:
            return False

        item_id_str = str(item_id)
        key = f"{TODO_ITEM_KEY_PREFIX}{item_id_str}"

        self.cache.delete(key)

        self.cache.delete(ALL_TODOS_KEY)

        for i, t in enumerate(self.todos):
            if str(t.item_id) == item_id_str:
                del self.todos[i]
                break

        self._save_to_redis()

        if self.cache.get(key) is not None:
            print(f"Warning: Item {item_id} could not be deleted from Redis!")
            return False

        return True

    def list_all(self):
        """
        Lists all TodoItems in the repository from Redis.

        :return: A list of all TodoItem instances in the repository.
        """
        cached_todos = self.cache.get(ALL_TODOS_KEY)
        if cached_todos:
            # Redis'ten alınan todos listesini TodoItem nesnelerine dönüştür
            self.todos = [TodoItem(**todo) if isinstance(todo, dict) else todo for todo in cached_todos]
            return self.todos

        # Eğer ALL_TODOS_KEY yoksa, bellek içindeki listeyi kullan ve Redis'e kaydet
        self._save_to_redis()
        return self.todos

    def _save_to_redis(self):
        """
        Saves the current list of todos to Redis.
        """
        self.cache.set(ALL_TODOS_KEY, self.todos)

        for todo in self.todos:
            self.cache.set(f"{TODO_ITEM_KEY_PREFIX}{todo.item_id}", todo)

    def _load_from_redis(self):
        """
        Loads todos from Redis.

        :return: A list of TodoItem instances.
        """
        cached_todos = self.cache.get(ALL_TODOS_KEY)
        if cached_todos:
            return [TodoItem(**todo) if isinstance(todo, dict) else todo for todo in cached_todos]
        return []

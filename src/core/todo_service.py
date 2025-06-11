import uuid

from src.config.redis_config import ALL_TODOS_KEY, TODO_ITEM_KEY_PREFIX
from src.core.elasticsearch_client import ElasticsearchClient
from src.core.redis_cache import RedisCache
from src.model.todo_item import TodoItem


class TodoService:
    def __init__(self, repository):
        """
        Initializes the TodoService with a repository to manage TodoItems.

        :param repository: A repository object that manages TodoItem instances.
        """
        self.repository = repository
        self.cache = RedisCache()
        self.es_client = ElasticsearchClient()

    def get_all_todos(self):
        """
        Retrieves all TodoItems from Redis.

        :return: A list of all TodoItems.
        """
        return self.repository.list_all()

    def get_todo_by_id(self, item_id):
        """
        Gets a todo item by its ID.

        :param item_id: The ID of the todo item to retrieve.
        :return: TodoItem if found, None otherwise.
        """
        return self.repository.find_by_id(item_id)

    def create_todo(self, title, description, due_date):
        """
        Creates a new TodoItem with the given details and adds it to the repository.

        :param title: The title of the TodoItem.
        :param description: A brief description of the TodoItem.
        :param due_date: The due date of the TodoItem.
        :return: The created TodoItem instance.
        """
        unique_id = str(uuid.uuid4())

        todo = TodoItem(unique_id, title, description, due_date)
        self.repository.add(todo)
        self.cache.delete(ALL_TODOS_KEY)
        self.es_client.index_todo(todo.__dict__)

        return todo

    def update_todo(self, item_id, **updates):
        """
        Updates an existing TodoItem with the given details.

        :param item_id: The ID of the todo item to update.
        :param updates: The details to update for the TodoItem.
        :return: The updated TodoItem instance, or None if the item does not exist.
        """
        todo = self.repository.update(item_id, **updates)
        if todo:
            self.es_client.index_todo(todo.__dict__)
        return todo

    def mark_as_completed(self, item_id):
        """
        Marks a todo item as completed by updating its status to 'completed'.

        :param item_id: The ID of the todo item to mark as completed.
        :return: The updated TodoItem instance, or None if the item does not exist.
        """
        todo = self.update_todo(item_id, status="completed")

        return todo

    def delete_todo(self, item_id):
        """
        Deletes an existing TodoItem with the given ID.

        :param item_id: The ID of the todo item to delete.
        :return: True if the item was deleted, False otherwise.
        """
        item_id_str = str(item_id)

        key = f"{TODO_ITEM_KEY_PREFIX}{item_id_str}"

        self.cache.delete(key)
        self.cache.delete(ALL_TODOS_KEY)

        result = self.repository.delete(item_id)
        if result:
            self.es_client.delete_todo(item_id)
        return result

class TodoItem:
    def __init__(self, item_id, title, description, due_date, status="pending"):
        self.item_id = item_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status

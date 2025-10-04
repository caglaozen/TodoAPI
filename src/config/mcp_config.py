MCP_SERVER_NAME = "todo-mcp-server"
MCP_SERVER_VERSION = "0.1.0"

TOOL_DESCRIPTIONS = {
    "list_todos": "Lists all todo items. Use when user wants to see/view/list their tasks or todos. Can be used with other tools in same request.",
    "create_todo": "Creates a new todo item. Use when user wants to add/create/remember a task. Keywords: 'ekle', 'add', 'yeni', 'oluştur'. Can be called multiple times in same request for multiple todos.",
    "get_todo_details": "Gets detailed information about a specific todo item by its ID. Use when user wants to see details of a particular todo.",
    "update_todo": "Updates an existing todo item. Use when user wants to change/update/modify title, description, or due date. Keywords: 'güncelle', 'update', 'değiştir'. Can be used with other tools.",
    "mark_completed": "Marks a todo item as completed. Use when user says they finished/completed/done a task. Keywords: 'tamamladım', 'bitti', 'yaptım', 'completed', 'done'. Can be used with other tools.",
    "delete_todo": "Deletes a todo item permanently. Use when user wants to remove/delete/sil a task. Keywords: 'sil', 'delete', 'kaldır', 'remove'. Can be used with other tools.",
    "search_todos": "Searches todos by keyword using Elasticsearch. Use when user wants to find/search todos containing specific words.",
    "strands_assistant": "⭐ AI-POWERED MULTI-STEP: Advanced assistant with autonomous reasoning. Use for COMPLEX requests requiring multiple steps. Examples: 'update X and delete Y', 'create 3 todos and mark completed ones', 'find work todos and organize them'. Automatically plans and executes operations. Supports English and Turkish.",
}

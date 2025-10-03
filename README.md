# Todo Application

This is a Python-based Todo application that provides functionality to manage todo items. It includes a RESTful API for CRUD operations, Redis-based storage, Elasticsearch search capabilities, AI agent integration, and MCP (Model Context Protocol) server for Claude Desktop integration. The project is built using Flask for the API, and it utilizes a modular design with services and repositories.

## Features

- **Create, Read, Update, and Delete (CRUD)**: Manage your todos with ease.
- **Redis Storage**: Persist todo items in Redis for fast access.
- **Redis Caching**: Efficient data retrieval with Redis-based caching.
- **Elasticsearch Integration**: Full-text search capabilities for finding todos.
- **AI Agent Integration**: Multilingual Gemini-powered agent for natural language todo management.
- **MCP Server**: Claude Desktop integration with 8 tools for seamless AI interaction.
- **Mark As Completed**: Quickly mark todo items as completed.
- **RESTful API**: Access the features programmatically using HTTP methods.
- **Unit Testing**: Comprehensive tests for both the repository and service layers.

## Project Structure

```
TodoAPI/
├── Dockerfile                           # Docker configuration
├── docker-compose.yml                  # Docker Compose with Redis, Elasticsearch
├── requirements.txt                    # Project dependencies
├── Makefile                            # Common commands (test, format, etc.)
├── src/
│   ├── app.py                          # Flask app with REST API endpoints
│   ├── dev_ui.py                       # Development UI for agent testing
│   ├── config/
│   │   ├── redis_config.py             # Redis configuration
│   │   ├── elasticsearch_config.py     # Elasticsearch configuration
│   │   └── mcp_config.py               # MCP server configuration
│   ├── core/
│   │   ├── todo_service.py             # Business logic for managing todos
│   │   ├── redis_cache.py              # Redis caching layer
│   │   └── elasticsearch_client.py     # Elasticsearch search client
│   ├── model/
│   │   └── todo_item.py                # TodoItem class definition
│   ├── repository/
│   │   └── todo_repository.py          # Repository for data persistence
│   ├── agent/
│   │   ├── root_agent.py               # Root agent entry point
│   │   ├── todo_agent.py               # Gemini-powered todo agent
│   │   └── todo_tools.py               # Agent tools for todo operations
│   └── todo_mcp/
│       ├── mcp_server.py               # MCP server for Claude Desktop
│       └── tools/
│           └── todo_tools.py           # MCP tool implementations
└── test/
    └── unit/
        ├── test_todo_service.py        # Unit tests for TodoService
        └── test_todo_repository.py     # Unit tests for TodoRepository
```

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Docker Installation

You can also run this application using Docker, which ensures consistent environments across different systems.

1. **Build the Docker Image**
   ```bash
   docker build -t todo-api .

2. **Run with Docker Compose**
   ```bash
   docker-compose up
    ```

## Usage

1. **Set the PYTHONPATH** 
   - Ensure that the `src` folder is recognized as a module. Run the following command to set the `PYTHONPATH`:
      ```bash
      export PYTHONPATH=$PYTHONPATH:/path/to/your/project/src   
     ```
   - Replace /path/to/your/project/ with the actual path to the project directory.

2. **Run the Application**
   - Navigate to the project root directory and run the app:
      ```bash
      cd /path/to/your/project
      python src/app.py
      ```
3. **API Endpoints**

    - **Create Todo**
        - `POST /todos`
        - Request Body:
          ```json
          {
            "title": "Task Title",
            "description": "Task Description",
            "due_date": "YYYY-MM-DD"
          }
          ```

    - **Update Todo**
        - `PUT /todos/<item_id>`
        - Request Body:
          ```json
          {
            "title": "Updated Title",
            "description": "Updated Description",
            "due_date": "YYYY-MM-DD",
            "status": "completed"
          }
          ```

    - **Delete Todo**
        - `DELETE /todos/<item_id>`

    - **List Todos**
        - `GET /todos`

    - **Mark as Completed**
        - `PUT /todos/<item_id>/complete`

    - **Search Todos**
        - `GET /todos/search?q=keyword`

## AI Agent Integration

The application includes a Gemini-powered AI agent that allows you to manage todos using natural language in multiple languages (English, Turkish, etc.).

### Prerequisites

- Google API Key with Gemini access
- Docker running (for Redis and Elasticsearch)

### Setup Steps

1. **Get a Google API Key**
   - Visit https://aistudio.google.com/apikey
   - Create a new API key
   - Copy the API key

2. **Set the API Key as Environment Variable**
   ```bash
   export GOOGLE_API_KEY="your-api-key-here"
   ```

   Or add it to your shell profile (~/.zshrc or ~/.bashrc):
   ```bash
   echo 'export GOOGLE_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Start Docker Services**
   ```bash
   docker-compose up -d
   ```

4. **Start the Flask API**
   ```bash
   python src/app.py
   ```
   The API will run on http://localhost:8000

5. **Start the Agent UI**
   ```bash
   python src/dev_ui.py
   ```
   The UI will be available at http://localhost:7860

6. **Open Your Browser**
   - Navigate to http://localhost:7860
   - Start chatting with the agent in natural language!

### Agent Features

- **Multilingual Support**: Works in English, Turkish, and other languages
- **Natural Language**: Understands phrases like "add shopping to tomorrow" or "yarın spor yapmayı ekle"
- **Smart Date Parsing**: Recognizes "today", "tomorrow", "next week", "bugün", "yarın", etc.
- **Search Capability**: Find todos using Elasticsearch full-text search
- **Conversational Interface**: Friendly responses with emojis and helpful suggestions

### Example Interactions

```
User: "I need to exercise tomorrow"
Agent: ✅ Creates a todo with due_date="2025-10-04"

User: "show my todos"
Agent: 📋 Lists all todos with formatted output

User: "find todos about shopping"
Agent: 🔍 Searches using Elasticsearch and shows matching todos

User: "yarın toplantı var saat 14:00'te"
Agent: ✅ Creates todo in Turkish: "toplantı" with description "saat 14:00'te"

User: "mark the first todo as completed"
Agent: ✅ Marks the todo as completed

User: "delete shopping todo"
Agent: 🗑️ Deletes the todo with title containing "shopping"
```

## MCP (Model Context Protocol) Integration

The application provides an MCP server that allows Claude Desktop to directly interact with your todos. This means you can manage your todos by simply chatting with Claude!

### Prerequisites

- Claude Desktop installed (download from https://claude.ai/download)
- Docker running (for Redis and Elasticsearch)
- Flask API running

### Setup Steps

1. **Install Claude Desktop**
   - Download from https://claude.ai/download
   - Install and open Claude Desktop

2. **Start Required Services**
   ```bash
   # Start Docker services (Redis + Elasticsearch)
   docker-compose up -d

   # Start Flask API
   python src/app.py
   ```
   Keep the Flask API running in a terminal.

3. **Get Your Project's Absolute Path**
   ```bash
   pwd
   ```
   Copy the output (e.g., `/Users/yourusername/Desktop/Codes/TodoAPI`)

4. **Configure Claude Desktop**
   - Open Claude Desktop
   - Click on the settings icon (⚙️) in the bottom-left
   - Go to "Developer" section
   - Click "Edit Config" button
   - This will open `claude_desktop_config.json` in your editor

5. **Add MCP Server Configuration**
   Replace the file contents with:
   ```json
   {
     "mcpServers": {
       "todo-mcp-server": {
         "command": "python",
         "args": ["/YOUR/ABSOLUTE/PATH/TodoAPI/src/todo_mcp/mcp_server.py"]
       }
     }
   }
   ```
   **Important**: Replace `/YOUR/ABSOLUTE/PATH/TodoAPI` with the path you copied in step 3.

   Example for macOS:
   ```json
   {
     "mcpServers": {
       "todo-mcp-server": {
         "command": "python",
         "args": ["/Users/yourusername/Desktop/Codes/TodoAPI/src/todo_mcp/mcp_server.py"]
       }
     }
   }
   ```

6. **Save and Restart Claude Desktop**
   - Save the config file
   - Completely quit Claude Desktop (Cmd+Q on Mac, or File → Quit)
   - Reopen Claude Desktop

7. **Verify Connection**
   - Look for a small hammer icon (🔨) in the input box at the bottom
   - This indicates MCP tools are connected
   - Or just ask Claude: "Can you list my todos?"

### Available MCP Tools

The MCP server provides 8 tools:

1. **list_todos**: List all todo items
2. **create_todo**: Create a new todo (supports natural language dates)
3. **get_todo_details**: Get details of a specific todo by ID
4. **update_todo**: Update an existing todo
5. **mark_completed**: Mark a todo as completed
6. **delete_todo**: Delete a todo
7. **search_todos**: Search todos using Elasticsearch
8. **batch_operations**: Execute multiple operations in a single call (recommended for efficiency)

### How to Use

Once configured, simply chat with Claude Desktop naturally. Claude will automatically use the MCP tools to manage your todos.

**Example Conversations:**

```
You: "Show me my todos for today"
Claude: *Uses list_todos tool and displays your todos*

You: "Add a meeting tomorrow at 2pm"
Claude: *Uses create_todo tool* ✅ Created todo "Meeting" for 2025-10-04 with description "2pm"

You: "Mark shopping as completed"
Claude: *Uses mark_completed tool* ✅ Marked "Shopping" as completed

You: "Search for todos about project"
Claude: *Uses search_todos tool* 🔍 Found 3 todos containing "project"

You: "Delete all old todos"
Claude: *Uses batch_operations tool* 🗑️ Deleted 5 old todos
```

**Multiple Operations at Once:**

You can ask Claude to do multiple things in one message:

```
You: "Do these things:
1. Add 'Buy groceries' for today
2. Mark 'Exercise' as completed
3. Delete 'Old task'
4. Update 'Meeting' to tomorrow at 3pm"

Claude: *Uses batch_operations tool to execute all at once*
✅ All operations completed successfully!
```

**Smart Features:**

- **Title-based lookup**: You don't need UUIDs, just say "mark shopping as completed"
- **Case-insensitive**: Works with "Shopping", "shopping", or "SHOPPING"
- **Natural dates**: "today", "tomorrow", "next week" all work
- **Multiple languages**: Works in Turkish too - "yarın toplantı ekle"

### Troubleshooting

**If tools don't appear:**
1. Make sure Flask API is running (`python src/app.py`)
2. Check that Docker containers are running (`docker-compose ps`)
3. Verify config path is absolute (not relative)
4. Check MCP server logs for errors
5. Restart Claude Desktop completely

**If operations fail:**
1. Ensure Redis is running: `docker ps | grep redis`
2. Ensure Elasticsearch is running: `docker ps | grep elasticsearch`
3. Check Flask API is accessible: `curl http://localhost:8000/todos`

## Testing

Run the unit tests to ensure everything is working as expected:
```bash
make test
```

## Code Style

We are using [Black](https://black.readthedocs.io/en/stable/) for code formatting and
[isort](https://pycqa.github.io/isort/index.html) for sorting the import statements. Please read the
[Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).

You can install them in your global environment using the following command to use it across all projects
and avoid shipping it with the project.

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install black
pipx install isort
```

### Style Checking

Run the style checker in dry-run mode to print the files that need to be formatted:
```bash
make style-check
```

Run the style checker and format the files:
```bash
make format
```

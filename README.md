# Todo Application

This is a Python-based Todo application that provides functionality to manage todo items. It includes a RESTful API for CRUD operations, JSON-based data storage, and unit tests to ensure functionality. The project is built using Flask for the API, and it utilizes a modular design with services and repositories.

## Features

- **Create, Read, Update, and Delete (CRUD)**: Manage your todos with ease.
- **Redis Storage**: Persist todo items in Redis for fast access.
- **Redis Caching**: Efficient data retrieval with Redis-based caching.
- **Mark As Completed**: Quickly mark todo items as completed.
- **RESTful API**: Access the features programmatically using HTTP methods.
- **Unit Testing**: Comprehensive tests for both the repository and service layers.

## Project Structure

```
TodoAPI/
├── Dockerfile                  # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── requirements.txt           # Project dependencies
├── src/
│   ├── core/
│   │   └── todo_service.py     # Business logic for managing todos
│   ├── model/
│   │   └── todo_item.py        # TodoItem class definition
│   ├── repository/
│   │   └── todo_repository.py  # Repository for data persistence
│   └── main.py                 # Flask app defining API endpoints
│
└── tests/
    ├── test_todo_service.py    # Unit tests for TodoService
    └── test_todo_repository.py # Unit tests for TodoRepository
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

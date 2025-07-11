"""
Todo Agent using Google ADK.
This agent can manage todo items through natural language conversation.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables.
load_dotenv()


def get_todo_count() -> dict:
    """
    Returns the current number of todo items.
    This is a simple test tool to verify ADK is working.
    
    Returns:
        dict: A dictionary containing status and count information.
    """
    return {
        "status": "success",
        "message": "Bu sadece test tool'u! Şu anda 5 todo item'ın var.",
        "count": 5
    }


def create_simple_todo(title: str) -> dict:
    """
    Creates a simple todo item (mock implementation for now).
    
    Args:
        title (str): The title of the todo item to create.
        
    Returns:
        dict: A dictionary containing the created todo information.
    """
    return {
        "status": "success", 
        "message": f"'{title}' adında yeni bir todo oluşturuldu!",
        "todo_id": "test-123",
        "title": title
    }


# Business logic agent definition.
todo_agent = Agent(
    name="todo_assistant",
    model="gemini-2.0-flash",
    description="Türkçe konuşan Todo listesi yönetim asistanı",
    instruction=(
        "Sen bir todo listesi yönetim asistanısın. Türkçe konuşuyorsun ve çok yardımseversin. "
        "Kullanıcı todo'larıyla ilgili isteklerde bulunduğunda, mevcut tool'ları kullanarak "
        "ona yardım ediyorsun. Samimi ve arkadaşça bir ton kullan."
    ),
    tools=[
        get_todo_count,
        create_simple_todo
    ]
)

print("✅ Todo Agent (business logic) başarıyla oluşturuldu!") 
"""
Simple ADK Agent - All in one file.
Gerçek Todo API entegrasyonu için hazır.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables.
load_dotenv()


def get_todo_count() -> dict:
    """
    Returns the current number of todo items.
    Bu tool gerçek API'ya bağlanacak.
    
    Returns:
        dict: A dictionary containing status and count information.
    """
    return {
        "status": "success",
        "message": "Şu anda 5 todo item'ın var. (Test verisi - yakında gerçek API'dan gelecek)",
        "count": 5
    }


def create_todo_item(title: str, description: str = "", due_date: str = "") -> dict:
    """
    Creates a new todo item.
    Yakında gerçek TodoService'e bağlanacak.
    
    Args:
        title (str): Todo başlığı (zorunlu)
        description (str): Todo açıklaması (opsiyonel)
        due_date (str): Bitiş tarihi (opsiyonel, YYYY-MM-DD formatında)
        
    Returns:
        dict: Oluşturulan todo bilgileri
    """
    # Yakında burası gerçek API çağrısı olacak:
    # from core.todo_service import TodoService
    # service = TodoService(repository)  
    # todo = service.create_todo(title, description, due_date)
    
    return {
        "status": "success",
        "message": f"'{title}' todo'su başarıyla oluşturuldu!",
        "todo": {
            "id": "temp-id-123",
            "title": title,
            "description": description,
            "due_date": due_date,
            "status": "pending"
        }
    }


def list_all_todos() -> dict:
    """
    Lists all todo items.
    Yakında gerçek API'dan gelecek.
    
    Returns:
        dict: Tüm todo'ların listesi
    """
    # Mock data - yakında gerçek API'dan gelecek
    mock_todos = [
        {"id": "1", "title": "Market alışverişi", "status": "pending", "due_date": "2024-06-20"},
        {"id": "2", "title": "Doktor randevusu", "status": "completed", "due_date": "2024-06-18"},
        {"id": "3", "title": "Proje teslimi", "status": "pending", "due_date": "2024-06-25"}
    ]
    
    return {
        "status": "success",
        "message": f"{len(mock_todos)} todo bulundu",
        "todos": mock_todos
    }


def mark_todo_completed(todo_id: str) -> dict:
    """
    Marks a todo as completed.
    
    Args:
        todo_id (str): Tamamlanacak todo'nun ID'si
        
    Returns:
        dict: İşlem sonucu
    """
    return {
        "status": "success",
        "message": f"Todo (ID: {todo_id}) başarıyla tamamlandı olarak işaretlendi!",
        "todo_id": todo_id
    }


# ADK Agent Definition - Tek dosyada, import sorunu yok.
root_agent = Agent(
    name="todo_assistant",
    model="gemini-2.0-flash",
    description="Türkçe konuşan gelişmiş Todo yönetim asistanı",
    instruction=(
        "Sen TodoAPI projesinin AI asistanısın. Türkçe konuşuyorsun ve çok yardımseversin. "
        "Kullanıcılar senden todo'larını yönetmelerini isteyebilir:\n"
        "- Todo oluşturma: 'Yeni todo ekle', 'Market alışverişi todo'su oluştur'\n"
        "- Todo listeleme: 'Todo'larımı göster', 'Hangi işlerim var?'\n"
        "- Todo tamamlama: 'İlk todo'yu tamamla', 'ID: 123 olan todo'yu bitir'\n"
        "- Todo sayma: 'Kaç tane todo'um var?'\n\n"
        "Her zaman samimi ve arkadaşça ol. Tool çağrılarından sonra sonuçları açık şekilde açıkla."
    ),
    tools=[
        get_todo_count,
        create_todo_item, 
        list_all_todos,
        mark_todo_completed
    ]
)

print("✅ Todo Assistant Agent hazır! (Single file approach)") 
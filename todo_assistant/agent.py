"""
Todo Assistant Agent.
Gerçek Redis ve Elasticsearch entegrasyonu ile çalışan AI asistan.
"""

import os
import sys
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables.
load_dotenv()

# Add parent directories to path for API integration.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, parent_dir)
sys.path.insert(0, src_dir)

# Set environment variables for TodoService (Elasticsearch and Redis).
os.environ['ELASTICSEARCH_HOST'] = os.getenv('ELASTICSEARCH_HOST', 'localhost')
os.environ['ELASTICSEARCH_PORT'] = os.getenv('ELASTICSEARCH_PORT', '9200')
os.environ['REDIS_HOST'] = os.getenv('REDIS_HOST', 'localhost')
os.environ['REDIS_PORT'] = os.getenv('REDIS_PORT', '6379')

# Import real TodoService and dependencies.
try:
    from src.core.todo_service import TodoService
    from src.repository.todo_repository import TodoRepository
    
    # Initialize real services.
    repository = TodoRepository()
    todo_service = TodoService(repository)
    print("🚀 TodoService (Redis + Elasticsearch) başarıyla yüklendi!")
except ImportError as e:
    print(f"⚠️ TodoService import hatası: {e}")
    todo_service = None
    repository = None
except Exception as e:
    print(f"⚠️ Service başlatma hatası: {e}")
    todo_service = None
    repository = None


def get_todo_count() -> dict:
    """
    Returns the current number of todo items from Redis.
    
    Returns:
        dict: A dictionary containing status and count information.
    """
    try:
        if todo_service:
            todos = todo_service.get_all_todos()
            count = len(todos)
            return {
                "status": "success",
                "message": f"Redis'ten {count} todo bulundu! 📊",
                "count": count
            }
        else:
            return {
                "status": "error", 
                "message": "TodoService bağlantısı yapılamadı ❌",
                "count": 0
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Redis hatası: {str(e)} ⚠️",
            "count": 0
        }


def create_todo_item(title: str, description: str = "", due_date: str = "") -> dict:
    """
    Creates a new todo item in Redis and Elasticsearch.
    
    Args:
        title (str): Todo başlığı (zorunlu)
        description (str): Todo açıklaması (opsiyonel)
        due_date (str): Bitiş tarihi (opsiyonel, YYYY-MM-DD formatında)
        
    Returns:
        dict: Oluşturulan todo bilgileri
    """
    try:
        if todo_service:
            todo = todo_service.create_todo(title, description, due_date)
            
            return {
                "status": "success",
                "message": f"✅ '{title}' Redis ve Elasticsearch'e kaydedildi!",
                "todo": {
                    "id": todo.item_id,
                    "title": todo.title,
                    "description": todo.description,
                    "due_date": todo.due_date,
                    "status": todo.status
                }
            }
        else:
            return {
                "status": "error",
                "message": "TodoService bağlantısı yapılamadı ❌"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Todo oluşturma hatası: {str(e)} ⚠️"
        }


def list_all_todos() -> dict:
    """
    Lists all todo items from Redis.
    
    Returns:
        dict: Tüm todo'ların listesi
    """
    try:
        if todo_service:
            todos = todo_service.get_all_todos()
            todo_list = []
            for todo in todos:
                todo_list.append({
                    "id": todo.item_id,
                    "title": todo.title,
                    "description": todo.description,
                    "status": todo.status,
                    "due_date": todo.due_date
                })
            
            return {
                "status": "success",
                "message": f"📋 Redis'ten {len(todos)} todo getirildi!",
                "todos": todo_list,
                "total_count": len(todos)
            }
        else:
            return {
                "status": "error",
                "message": "TodoService bağlantısı yapılamadı ❌",
                "todos": [],
                "total_count": 0
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Todo listesi hatası: {str(e)} ⚠️",
            "todos": [],
            "total_count": 0
        }


def mark_todo_completed(todo_id: str) -> dict:
    """
    Marks a todo as completed in Redis and Elasticsearch.
    
    Args:
        todo_id (str): Tamamlanacak todo'nun ID'si
        
    Returns:
        dict: İşlem sonucu
    """
    try:
        if todo_service:
            updated_todo = todo_service.mark_as_completed(todo_id)
            if updated_todo:
                return {
                    "status": "success",
                    "message": f"✅ Todo (ID: {todo_id}) Redis ve Elasticsearch'te tamamlandı!",
                    "todo_id": todo_id,
                    "new_status": "completed"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Todo (ID: {todo_id}) bulunamadı ❌"
                }
        else:
            return {
                "status": "error",
                "message": "TodoService bağlantısı yapılamadı ❌"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Todo tamamlama hatası: {str(e)} ⚠️"
        }


def delete_todo_item(todo_id: str) -> dict:
    """
    Deletes a todo item from Redis and Elasticsearch.
    
    Args:
        todo_id (str): Silinecek todo'nun ID'si
        
    Returns:
        dict: İşlem sonucu
    """
    try:
        if todo_service:
            success = todo_service.delete_todo(todo_id)
            if success:
                return {
                    "status": "success", 
                    "message": f"🗑️ Todo (ID: {todo_id}) Redis ve Elasticsearch'ten silindi!",
                    "todo_id": todo_id
                }
            else:
                return {
                    "status": "error",
                    "message": f"Todo (ID: {todo_id}) bulunamadı veya silinemedi ❌"
                }
        else:
            return {
                "status": "error",
                "message": "TodoService bağlantısı yapılamadı ❌"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Todo silme hatası: {str(e)} ⚠️"
        }


# ADK Agent Definition.
root_agent = Agent(
    name="todo_assistant",
    model="gemini-2.0-flash",
    description="Türkçe konuşan Todo API asistanı - Redis ve Elasticsearch entegrasyonlu",
    instruction=(
        "Sen TodoAPI projesinin AI asistanısın! Türkçe konuşuyorsun ve çok yardımseversin. "
        "Kullanıcıların todo'larını Redis ve Elasticsearch ile yönetiyorsun:\n\n"
        
        "🎯 **Ana İşlevlerin:**\n"
        "• 📊 Todo sayma: 'Kaç todo'um var?', 'Todo sayımı söyle' - Redis'ten gerçek veri\n"
        "• ➕ Todo oluşturma: 'Yeni todo ekle', 'Market alışverişi todo'su oluştur' - Redis'e kaydeder, Elasticsearch'e indexler\n"
        "• 📋 Todo listeleme: 'Todo'larımı göster', 'Tüm işlerimi listele' - Redis'ten tam liste\n"
        "• ✅ Todo tamamlama: '1 numaralı todo'yu tamamla' - Redis'te günceller, Elasticsearch'e yansıtır\n"
        "• 🗑️ Todo silme: '2 numaralı todo'yu sil' - Redis'ten ve Elasticsearch'ten kaldırır\n\n"
        
        "💡 **Şu an gerçek Redis/TodoService/Elasticsearch ile çalışıyorsun!**\n\n"
        
        "📋 **Davranış Kuralların:**\n"
        "• Her zaman samimi ve arkadaşça ol\n"
        "• Tool çağrılarından sonra sonuçları açık şekilde açıkla\n"
        "• Redis ve Elasticsearch işlemlerini belirt\n"
        "• Emoji kullanarak cevapları görsel olarak zenginleştir\n"
        "• Kullanıcı belirsiz istekte bulunursa, açıklama iste\n"
        "• Başarılı işlemlerden sonra kullanıcıyı tebrik et\n"
        "• Hata durumlarında açık bilgi ver"
    ),
    tools=[
        get_todo_count,
        create_todo_item, 
        list_all_todos,
        mark_todo_completed,
        delete_todo_item
    ]
)

print("🚀 Todo Assistant Agent Redis + Elasticsearch ile hazır!") 
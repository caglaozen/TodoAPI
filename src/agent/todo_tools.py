"""
Todo Tools for Google ADK Agent.
Bu dosya agent'ın gerçek todo sistemine bağlanmasını sağlar.
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Optional

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.core.todo_service import TodoService
from src.repository.todo_repository import TodoRepository


# Singleton pattern: Tek bir service instance kullan
_service_instance = None


def get_service() -> TodoService:
    """TodoService singleton instance döndürür."""
    global _service_instance
    if _service_instance is None:
        repo = TodoRepository()
        _service_instance = TodoService(repo)
    return _service_instance


def parse_relative_date(date_string: str) -> str:
    """
    Türkçe tarih ifadelerini YYYY-MM-DD formatına çevirir.

    Args:
        date_string: "bugün", "yarın", "gelecek hafta" gibi ifadeler

    Returns:
        YYYY-MM-DD formatında tarih
    """
    today = datetime.now()
    date_lower = date_string.lower().strip()

    if date_lower in ["bugün", "today"]:
        return today.strftime("%Y-%m-%d")
    elif date_lower in ["yarın", "tomorrow"]:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_lower in ["gelecek hafta", "next week"]:
        return (today + timedelta(weeks=1)).strftime("%Y-%m-%d")
    elif date_lower in ["bu hafta sonu", "this weekend"]:
        # Cumartesi'ye kadar olan gün sayısını hesapla
        days_until_saturday = (5 - today.weekday()) % 7
        return (today + timedelta(days=days_until_saturday)).strftime("%Y-%m-%d")
    else:
        # Eğer tarih formatı verilmişse direkt döndür
        # Yoksa 7 gün sonrası default
        try:
            # YYYY-MM-DD formatında mı kontrol et
            datetime.strptime(date_string, "%Y-%m-%d")
            return date_string
        except:
            # Default: 7 gün sonra
            return (today + timedelta(days=7)).strftime("%Y-%m-%d")


# ============================================================================
# TOOL FUNCTIONS - Agent tarafından kullanılacak
# ============================================================================

def list_all_todos() -> dict:
    """
    Tüm todo'ları listeler.

    Returns:
        dict: Todo listesi ve durum bilgisi
    """
    try:
        service = get_service()
        todos = service.get_all_todos()

        if not todos:
            return {
                "status": "success",
                "message": "Todo listeniz boş. Yeni bir todo eklemek ister misiniz?",
                "count": 0,
                "todos": []
            }

        todo_list = []
        for todo in todos:
            todo_list.append({
                "id": todo.item_id,
                "title": todo.title,
                "description": todo.description,
                "due_date": todo.due_date,
                "status": todo.status
            })

        return {
            "status": "success",
            "message": f"Toplam {len(todos)} todo bulundu.",
            "count": len(todos),
            "todos": todo_list
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Todo'lar listelenirken hata oluştu: {str(e)}",
            "count": 0,
            "todos": []
        }


def get_todo_details(item_id: str) -> dict:
    """
    Belirli bir todo'nun detaylarını getirir.

    Args:
        item_id: Todo'nun ID'si

    Returns:
        dict: Todo detayları
    """
    try:
        service = get_service()
        todo = service.get_todo_by_id(item_id)

        if not todo:
            return {
                "status": "error",
                "message": f"'{item_id}' ID'li todo bulunamadı.",
                "todo": None
            }

        return {
            "status": "success",
            "message": "Todo detayları başarıyla getirildi.",
            "todo": {
                "id": todo.item_id,
                "title": todo.title,
                "description": todo.description,
                "due_date": todo.due_date,
                "status": todo.status
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Todo detayları getirilirken hata: {str(e)}",
            "todo": None
        }


def create_todo_item(title: str, description: str = "", due_date: str = "") -> dict:
    """
    Yeni bir todo oluşturur.

    Args:
        title: Todo başlığı (zorunlu)
        description: Todo açıklaması (opsiyonel)
        due_date: Bitiş tarihi - "bugün", "yarın" gibi ifadeler veya YYYY-MM-DD formatı (opsiyonel)

    Returns:
        dict: Oluşturulan todo bilgisi
    """
    try:
        # Tarih parsing
        if not due_date:
            parsed_date = parse_relative_date("gelecek hafta")
        else:
            parsed_date = parse_relative_date(due_date)

        service = get_service()
        todo = service.create_todo(
            title=title,
            description=description or "",
            due_date=parsed_date
        )

        return {
            "status": "success",
            "message": f"'{title}' todo'su başarıyla oluşturuldu! Bitiş tarihi: {parsed_date}",
            "todo": {
                "id": todo.item_id,
                "title": todo.title,
                "description": todo.description,
                "due_date": todo.due_date,
                "status": todo.status
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Todo oluşturulurken hata: {str(e)}",
            "todo": None
        }


def update_todo_item(
    item_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None
) -> dict:
    """
    Mevcut bir todo'yu günceller.

    Args:
        item_id: Güncellenecek todo'nun ID'si
        title: Yeni başlık (opsiyonel)
        description: Yeni açıklama (opsiyonel)
        due_date: Yeni bitiş tarihi (opsiyonel)

    Returns:
        dict: Güncellenmiş todo bilgisi
    """
    try:
        updates = {}
        if title:
            updates["title"] = title
        if description:
            updates["description"] = description
        if due_date:
            updates["due_date"] = parse_relative_date(due_date)

        if not updates:
            return {
                "status": "error",
                "message": "Güncellenecek bir alan belirtilmedi.",
                "todo": None
            }

        service = get_service()
        todo = service.update_todo(item_id, **updates)

        if not todo:
            return {
                "status": "error",
                "message": f"'{item_id}' ID'li todo bulunamadı.",
                "todo": None
            }

        return {
            "status": "success",
            "message": f"'{todo.title}' todo'su başarıyla güncellendi.",
            "todo": {
                "id": todo.item_id,
                "title": todo.title,
                "description": todo.description,
                "due_date": todo.due_date,
                "status": todo.status
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Todo güncellenirken hata: {str(e)}",
            "todo": None
        }


def mark_todo_completed(item_id: str) -> dict:
    """
    Bir todo'yu tamamlanmış olarak işaretler.

    Args:
        item_id: Tamamlanacak todo'nun ID'si

    Returns:
        dict: Güncellenen todo bilgisi
    """
    try:
        service = get_service()
        todo = service.mark_as_completed(item_id)

        if not todo:
            return {
                "status": "error",
                "message": f"'{item_id}' ID'li todo bulunamadı.",
                "todo": None
            }

        return {
            "status": "success",
            "message": f"✅ '{todo.title}' todo'su tamamlandı olarak işaretlendi!",
            "todo": {
                "id": todo.item_id,
                "title": todo.title,
                "description": todo.description,
                "due_date": todo.due_date,
                "status": todo.status
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Todo tamamlanırken hata: {str(e)}",
            "todo": None
        }


def delete_todo_item(item_id: str) -> dict:
    """
    Bir todo'yu siler.

    Args:
        item_id: Silinecek todo'nun ID'si

    Returns:
        dict: Silme işlemi sonucu
    """
    try:
        service = get_service()

        # Önce todo'yu bul (başlığını göstermek için)
        todo = service.get_todo_by_id(item_id)
        if not todo:
            return {
                "status": "error",
                "message": f"'{item_id}' ID'li todo bulunamadı.",
                "deleted": False
            }

        title = todo.title
        result = service.delete_todo(item_id)

        if result:
            return {
                "status": "success",
                "message": f"🗑️ '{title}' todo'su başarıyla silindi.",
                "deleted": True
            }
        else:
            return {
                "status": "error",
                "message": "Todo silinirken bir hata oluştu.",
                "deleted": False
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Todo silinirken hata: {str(e)}",
            "deleted": False
        }


def search_todos(query: str) -> dict:
    """
    Todo'larda arama yapar (Elasticsearch kullanır).

    Args:
        query: Aranacak kelime veya cümle

    Returns:
        dict: Arama sonuçları
    """
    try:
        service = get_service()
        results = service.es_client.search_todos(query)
        hits = results["hits"]["hits"]

        if not hits:
            return {
                "status": "success",
                "message": f"'{query}' için sonuç bulunamadı.",
                "count": 0,
                "todos": []
            }

        todo_list = [hit["_source"] for hit in hits]

        return {
            "status": "success",
            "message": f"'{query}' için {len(hits)} sonuç bulundu.",
            "count": len(hits),
            "todos": todo_list
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Arama yapılırken hata: {str(e)}",
            "count": 0,
            "todos": []
        }

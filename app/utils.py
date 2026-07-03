"""Вспомогательные функции."""

import hashlib
import logging
from typing import Any

logger = logging.getLogger(__name__)


def get_hash(data: Any, length: int = 7) -> str:
    """
    Получить хеш строки SHA-512.
    
    Args:
        data: Данные для хеширования
        length: Длина результирующего хеша
        
    Returns:
        Хеш строка
    """
    try:
        hash_value = hashlib.sha512(str(data).encode('utf-8')).hexdigest()
        return hash_value[:length]
    except Exception as e:
        logger.error(f"Ошибка при хешировании данных: {e}")
        return "error"


def instance_attributes(obj: Any) -> dict:
    """
    Получить словарь атрибутов экземпляра объекта.
    
    Args:
        obj: Объект для анализа
        
    Returns:
        Словарь {имя_атрибута: значение}
    """
    try:
        return vars(obj)
    except TypeError:
        pass

    # Если нет __dict__, пробуем __slots__
    try:
        slots = obj.__slots__
    except AttributeError:
        return {}
    
    # Собираем все атрибуты из __slots__
    attrs = {}
    for name in slots:
        try:
            attrs[name] = getattr(obj, name)
        except AttributeError:
            continue
    
    return attrs

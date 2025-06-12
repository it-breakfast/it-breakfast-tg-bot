import json
import os
from datetime import datetime
from threading import Lock

LIMITS_FILE = 'TelegramBot/helpers/user_limits.json'

_limits_lock = Lock()

def _load_limits():
    if not os.path.exists(LIMITS_FILE):
        return {}
    with open(LIMITS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return {}

def _save_limits(limits):
    with open(LIMITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(limits, f, ensure_ascii=False)

def get_and_increment_limit(user_id: int) -> bool:
    """
    Проверяет, не превысил ли пользователь лимит, и увеличивает счётчик, если не превысил.
    Возвращает True, если можно использовать, иначе False.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    with _limits_lock:
        limits = _load_limits()
        user_limits = limits.get(str(user_id), {})
        if user_limits.get('date') != today:
            user_limits = {'date': today, 'count': 0}
        user_limits['count'] += 1
        limits[str(user_id)] = user_limits
        _save_limits(limits)
    return user_limits['count']

def reset_limits():
    """
    Сбрасывает все лимиты (например, по расписанию).
    """
    with _limits_lock:
        _save_limits({}) 
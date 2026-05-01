import requests
import random
import time
from collections import deque
import re
from datetime import datetime
import logging
from typing import Optional, List, Dict, Tuple

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# База реальных User-Agent (50+ актуальных версий)
USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    
    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    
    # Firefox Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
    
    # Firefox Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:119.0) Gecko/20100101 Firefox/119.0",
    
    # Edge Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0",
    
    # Safari Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    
    # Chrome Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    
    # Firefox Linux
    "Mozilla/5.0 (X11; Linux i686; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0",
    
    # Mobile Chrome Android
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    
    # Mobile Safari iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    
    # Дополнительные варианты
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
]

# Добавляем еще User-Agent до 50+
EXTRA_AGENTS = [
    f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36"
    for v in range(100, 121)
]
USER_AGENTS.extend(EXTRA_AGENTS[:25])

class SmartUARequester:
    """Класс для умной подмены User-Agent с самообучением"""
    
    def __init__(self):
        self.white_list = []  # Успешные User-Agent
        self.black_list = set()  # Заблокированные User-Agent
        self.used_recent = deque(maxlen=5)  # Последние 5 использованных
        self.domain_errors = {}  # Счетчик ошибок по доменам
        self.base_delay = 1  # Базовая задержка в секундах
        
    def _is_blocked_response(self, response: requests.Response) -> Tuple[bool, str]:
        """
        Анализирует ответ на предмет блокировки.
        Возвращает (заблокирован, причина)
        """
        # Проверка статус-кода
        if response.status_code in [403, 429]:
            return True, f"HTTP {response.status_code}"
        
        if 500 <= response.status_code < 600:
            return True, f"Server error {response.status_code}"
        
        # Проверка HTML на наличие маркеров блокировки
        if response.text:
            text_lower = response.text.lower()
            blocked_markers = [
                'blocked', 'access denied', 'forbidden', 
                'captcha', 'robot', 'unusual traffic',
                'access denied', 'not allowed'
            ]
            
            for marker in blocked_markers:
                if marker in text_lower:
                    return True, f"Found '{marker}' in response"
        
        return False, "Success"
    
    def _select_user_agent(self) -> str:
        """Выбирает User-Agent на основе белого списка или случайный"""
        if self.white_list and random.random() < 0.7:  # 70% вероятность использовать белый список
            # Выбираем из белого списка, исключая последние использованные
            available = [ua for ua in self.white_list if ua not in self.used_recent]
            if available:
                return random.choice(available)
        
        # Выбираем случайный, исключая черный список и последние использованные
        available = [ua for ua in USER_AGENTS 
                    if ua not in self.black_list and ua not in self.used_recent]
        
        if not available:
            # Если нет доступных, игнорируем ограничения
            available = [ua for ua in USER_AGENTS if ua not in self.used_recent]
        
        return random.choice(available) if available else random.choice(USER_AGENTS)
    
    def _get_delay(self, domain: str) -> float:
        """Рассчитывает задержку на основе истории ошибок домена"""
        error_count = self.domain_errors.get(domain, 0)
        delay = self.base_delay * (2 ** error_count)  # Экспоненциальный рост
        return min(delay, 30)  # Максимум 30 секунд
    
    def _update_domain_errors(self, domain: str, was_blocked: bool):
        """Обновляет счетчик ошибок для домена"""
        if was_blocked:
            self.domain_errors[domain] = self.domain_errors.get(domain, 0) + 1
        else:
            if domain in self.domain_errors:
                self.domain_errors[domain] = max(0, self.domain_errors[domain] - 1)
    
    def fetch_with_smart_ua(self, url: str, max_retries: int = 5) -> Optional[str]:
        """
        Выполняет запрос с умной подменой User-Agent
        
        Args:
            url: Целевой URL
            max_retries: Максимальное количество попыток
        
        Returns:
            Текст ответа при успехе, иначе None
        """
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        
        for attempt in range(max_retries):
            # Выбираем User-Agent
            user_agent = self._select_user_agent()
            self.used_recent.append(user_agent)
            
            headers = {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # Задержка перед запросом
            delay = self._get_delay(domain)
            if attempt > 0:
                logger.info(f"Задержка перед попыткой {attempt + 1}: {delay:.2f} сек")
                time.sleep(delay)
            
            try:
                logger.info(f"Попытка {attempt + 1}/{max_retries} | UA: {user_agent[:50]}...")
                response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
                
                # Анализируем ответ
                is_blocked, reason = self._is_blocked_response(response)
                
                if not is_blocked and response.status_code == 200:
                    # Успешный ответ
                    logger.info(f"✅ УСПЕХ | Статус: {response.status_code} | Причина: {reason}")
                    
                    # Добавляем в белый список, если еще не там
                    if user_agent not in self.white_list:
                        self.white_list.append(user_agent)
                        # Ограничиваем размер белого списка
                        if len(self.white_list) > 20:
                            self.white_list.pop(0)
                    
                    # Обновляем счетчик ошибок
                    self._update_domain_errors(domain, False)
                    
                    return response.text
                else:
                    # Заблокированный ответ
                    logger.warning(f"❌ БЛОКИРОВКА | Статус: {response.status_code} | Причина: {reason} | UA: {user_agent}")
                    
                    # Добавляем в черный список
                    self.black_list.add(user_agent)
                    
                    # Если UA был в белом списке, удаляем оттуда
                    if user_agent in self.white_list:
                        self.white_list.remove(user_agent)
                    
                    # Обновляем счетчик ошибок
                    self._update_domain_errors(domain, True)
                    
                    # Если ответ содержит капчу, увеличиваем задержку
                    if 'captcha' in response.text.lower():
                        extra_delay = random.uniform(5, 10)
                        logger.info(f"Обнаружена капча, дополнительная задержка: {extra_delay:.2f} сек")
                        time.sleep(extra_delay)
                    
                    continue
                    
            except requests.RequestException as e:
                logger.error(f"❌ ОШИБКА ЗАПРОСА | Попытка {attempt + 1}: {str(e)}")
                self._update_domain_errors(domain, True)
                continue
        
        logger.error(f"❌ НЕ УДАЛОСЬ ПОЛУЧИТЬ ДАННЫЕ после {max_retries} попыток")
        return None
    
    def train_on_urls(self, urls: List[str], learning_requests: int = 10):
        """
        Обучающий режим: делает несколько запросов для поиска рабочих User-Agent
        
        Args:
            urls: Список URL для обучения
            learning_requests: Количество обучающих запросов
        """
        logger.info(f"🚀 НАЧАЛО ОБУЧЕНИЯ на {len(urls)} URL, {learning_requests} запросов")
        
        for i in range(learning_requests):
            url = random.choice(urls)
            logger.info(f"Обучение {i + 1}/{learning_requests}: {url}")
            
            result = self.fetch_with_smart_ua(url, max_retries=2)
            if result:
                logger.info(f"✅ Найден рабочий User-Agent (всего в белом списке: {len(self.white_list)})")
            
            # Пауза между обучающими запросами
            if i < learning_requests - 1:
                time.sleep(random.uniform(1, 3))
        
        logger.info(f"🏁 ОБУЧЕНИЕ ЗАВЕРШЕНО. Белый список: {len(self.white_list)} UA")


# Глобальная функция для простого использования
_smart_requester = SmartUARequester()

def fetch_with_smart_ua(url: str, max_retries: int = 5) -> Optional[str]:
    """
    Упрощенная функция для выполнения запроса с умной подменой User-Agent
    
    Args:
        url: Целевой URL
        max_retries: Максимальное количество попыток
    
    Returns:
        Текст ответа при успехе, иначе None
    """
    return _smart_requester.fetch_with_smart_ua(url, max_retries)


# Пример использования
if __name__ == "__main__":
    # Создаем экземпляр для демонстрации
    requester = SmartUARequester()
    
    # Пример 1: Тестовый запрос к httpbin
    print("\n" + "="*60)
    print("ПРИМЕР 1: Запрос к httpbin.org")
    print("="*60)
    result = requester.fetch_with_smart_ua("https://httpbin.org/user-agent")
    if result:
        print(f"Результат: {result[:200]}")
    
    # Пример 2: Обучение на нескольких URL
    print("\n" + "="*60)
    print("ПРИМЕР 2: Обучение на нескольких сайтах")
    print("="*60)
    
    test_urls = [
        "https://httpbin.org/headers",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/ip"
    ]
    
    requester.train_on_urls(test_urls, learning_requests=5)
    
    # Пример 3: Запрос после обучения
    print("\n" + "="*60)
    print("ПРИМЕР 3: Запрос после обучения")
    print("="*60)
    final_result = requester.fetch_with_smart_ua("https://httpbin.org/get")
    if final_result:
        print(f"Успешный ответ после обучения: {final_result[:300]}")
    
    # Статистика
    print("\n" + "="*60)
    print("СТАТИСТИКА")
    print("="*60)
    print(f"Белый список (успешные UA): {len(requester.white_list)}")
    print(f"Черный список (заблокированные UA): {len(requester.black_list)}")
    print(f"Счетчик ошибок по доменам: {requester.domain_errors}")
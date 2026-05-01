# 🚀 Smart User-Agent Rotator

### Интеллектуальная система обхода блокировок с самообучением

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Requests](https://img.shields.io/badge/Requests-2.31+-red.svg)](https://requests.readthedocs.io/)

---

## 📖 О проекте

**Smart User-Agent Rotator** — это Python-скрипт для автоматической подмены User-Agent с системой самообучения. Скрипт запоминает успешные и заблокированные User-Agent, адаптируется под каждый сайт и эффективно обходит блокировки.

---

## ✨ Возможности

| 🎯 | 🧠 | 🔄 | 🛡️ | ⏱️ | 📊 |
|---|---|---|---|---|---|
| **50+ реальных UA** | **Самообучение** | **Умная ротация** | **Анализ блокировок** | **Адаптивные задержки** | **Детальное логирование** |
| Chrome, Firefox, Edge, Safari | Белый + черный списки | Без повтора последних 5 | 403, 429, капча | Экспоненциальный рост | Цветной вывод |

---

## 📋 Требования

- Python 3.7 или выше
- Библиотека requests

---

## ⚡ Установка

# Клонируем репозиторий
    git clone https://github.com/LondoGrafSmith/smart-ua-rotator.git
    cd smart-ua-rotator

# Устанавливаем зависимости
    pip install -r requirements.txt
    
---

##
🚀 Быстрый старт
    
    python
    
    from smart_ua_rotator import fetch_with_smart_ua

    result = fetch_with_smart_ua("https://httpbin.org/user-agent")
    print(result)

📖 Использование
    
    python
    
    from smart_ua_rotator import SmartUARequester

    requester = SmartUARequester()
    result = requester.fetch_with_smart_ua("https://example.com", max_retries=5)

📖 Режим обучения

    pytnon
    
    from smart_ua_rotator import SmartUARequester
    requester = SmartUARequester()
    
    # Обучаемся на нескольких страницах
    urls = ["https://target-site.com", "https://target-site.com/page2"]
    requester.train_on_urls(urls, learning_requests=10)

    # Основной запрос
    result = requester.fetch_with_smart_ua("https://target-site.com/protected-page")

Настройка задержек
    
    python
    
    requester = SmartUARequester()
    requester.base_delay = 2  # задержка 2 секунды между попытками


💡 Примеры
Парсинг новостей

    python
    
    from smart_ua_rotator import SmartUARequester
    import time

    requester = SmartUARequester()
    requester.train_on_urls(["https://news-site.com"], learning_requests=5)

    articles = ["/article1", "/article2", "/article3"]

    for article in articles:
        content = requester.fetch_with_smart_ua(f"https://news-site.com{article}")
        if content:
            with open(f"{article}.html", "w", encoding="utf-8") as f:
                f.write(content)
        print(f"✅ Сохранено: {article}")
    time.sleep(2)

Работа с API
    
    python
    from smart_ua_rotator import SmartUARequester

    requester = SmartUARequester()
    success = 0

    for page in range(1, 21):
        result = requester.fetch_with_smart_ua(f"https://api.site.com/users?page={page}")
        if result:
            success += 1
            print(f"✅ Страница {page}: успешно")
        else:
            print(f"❌ Страница {page}: ошибка")

    print(f"📊 Итого: успешно {success}")

Сохранение состояния

    python
    
    import pickle
    from smart_ua_rotator import SmartUARequester

    # Сохраняем обученного requester
    requester = SmartUARequester()
    requester.train_on_urls(["https://example.com"], learning_requests=10)

    with open('requester_state.pkl', 'wb') as f:
        pickle.dump(requester, f)

    # Загружаем позже
    with open('requester_state.pkl', 'rb') as f:
        loaded = pickle.load(f)

    result = loaded.fetch_with_smart_ua("https://example.com/data")

📊 Логирование
Пример вывода в консоли:

    text
    2024-01-15 10:30:45 - INFO - 🚀 Попытка 1/5 | UA: Mozilla/5.0 (Windows NT 10.0...
    2024-01-15 10:30:46 - INFO - ✅ УСПЕХ | Статус: 200
    2024-01-15 10:30:48 - WARNING - ❌ БЛОКИРОВКА | Статус: 403
    2024-01-15 10:30:50 - INFO - 📊 Белый список: 12 UA
    2024-01-15 10:30:51 - INFO - 📈 Черный список: 3 UA

⚙️ Настройка
Добавление своих User-Agent

    python
    
    from smart_ua_rotator import USER_AGENTS

    USER_AGENTS.append("Mozilla/5.0 (Мой Браузер)")

Свои маркеры блокировки
Найдите в коде метод _is_blocked_response и добавьте в список:

    python
    
    blocked_markers = [
        'blocked',
        'access denied',
        'ваш_маркер',  # добавьте сюда
    ]

🐛 Решение проблем
Проблема: Все запросы блокируются

    python
    
    # Увеличьте задержки
    requester.base_delay = 5

    # Увеличьте обучение
    requester.train_on_urls(urls, learning_requests=20)

    # Добавьте паузу
    time.sleep(10)    

Проблема: Слишком медленно
    
    python
    
    # Уменьшите задержки
    requester.base_delay = 0.5

    # Уменьшите количество попыток
    result = fetch_with_smart_ua(url, max_retries=2)

Проблема: Ошибка import requests

    bash
    
    pip install requests 

 
---

## 🔒 Этика использования

| ✅ Рекомендуется | ❌ Запрещается |
|---|---|
| **Соблюдать robots.txt** | **Нарушать закон** |
| **Использовать разумные задержки** | 	**Перегружать серверы** |
| **Уважать авторские права** | **Красть контент** |
| **Использовать для обучения** | **Атаковать сайты** |

---

🤝 Вклад в проект

    Приветствуются улучшения!

    Форкните репозиторий

    Создайте ветку (git checkout -b feature/improvement)

    Закоммитьте изменения (git commit -m 'Add improvement')

    Запушьте (git push origin feature/improvement)

    Откройте Pull Request

⭐ Поддержка
Поставьте звезду на GitHub, если проект оказался полезным!

<div align="center">
Сделано с ❤️ для сообщества разработчиков
</div> 

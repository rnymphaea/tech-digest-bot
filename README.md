# 🤖 tech-digest-bot

[![Python](https://img.shields.io/badge/python-%3E=3.11-green?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-24-2496ED?logo=docker)](https://www.docker.com/)
[![RSS](https://img.shields.io/badge/RSS-Parser-orange?logo=rss)](https://habr.com/ru/rss/)  

---

## 📋 Оглавление
- [🌟 Обзор проекта](#-обзор-проекта)
- [🚀 Основные возможности](#-основные-возможности)
- [⚙️ Технологический стек](#️-технологический-стек)
- [🏗️ Структура проекта](#️-структура-проекта)
- [🚀 Быстрый старт](#-быстрый-старт)

---

## 🌟 Обзор проекта

**tech-digest-bot** — это Telegram-бот для подписки на новости по категориям.  
Он использует RSS-потоки (например, Хабр) и по расписанию присылает новые статьи подписанным пользователям.  

---

## 🚀 Основные возможности

### 📚 Подписки на категории
- Пользователь выбирает интересующие категории
- Можно подписаться на несколько категорий сразу
- Возможность сбросить все подписки одной кнопкой  

### 📰 Новости и статьи
- Парсинг RSS
- Отправка свежих публикаций по категориям
- Умная фильтрация, чтобы статьи не дублировались  

### ⏰ Планировщик
- Автоматическая отправка статей по расписанию
- Используется `APScheduler` на базе `asyncio`  

---

## ⚙️ Технологический стек

- **Python 3.11+**
- **Aiogram 3.x** — работа с Telegram Bot API
- **APScheduler** — планировщик задач
- **Feedparser** — парсинг RSS
- **Docker + Docker Compose** — контейнеризация 

---

## 🏗️ Структура проекта

```
.
├── docker-compose.yml
├── Dockerfile
├── dump.json
├── Makefile
├── poetry.lock
├── pyproject.toml
└── src
    ├── bot
    │   ├── config.py               # конфигурация бота
    │   ├── handlers                # хендлеры команд и callback'ов
    │   │   └── news.py
    │   ├── keyboards               # клавиатуры
    │   │   └── news_keyboards.py
    │   ├── main.py                 # точка входа
    │   ├── scheduler.py            # планировщик APScheduler
    │   └── states.py               # состояния бота
    ├── parsers                     # парсеры новостей
    │   └── habr_rss.py
    ├── services                    # сервисы
    │   └── subscription_service.py # сервис подписок
    └── storage                     # работа с хранилищами
        ├── local                   # локальное хранилище
        │   └── storage.py
        └── repository.py           # интерфейс хранилища
```
## 🚀 Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone https://github.com/rnymphaea/tech-digest-bot.git
cd tech-digest-bot 
```
### 2. Создать файл с токеном для бота и указать его в docker-compose.yml 
### 3. Запустить с помощью make 
```bash
make
```

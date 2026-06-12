# Students Life - Django Monolith Migration

Международный образовательный портал, мигрированный со стека Strapi CMS + MongoDB + React на Django монолит.

## Структура проекта

```
students_life_project/
├── students_life/          # Основной проект Django
│   ├── settings.py         # Настройки (i18n, БД, безопасность)
│   ├── urls.py             # URL конфигурация с i18n_patterns
│   └── wsgi.py             # WSGI конфиг
├── core/                   # Главная страница, отзывы, документы, формы
├── geo/                    # Страны и города
├── company/                # Офисы и сотрудники
├── news/                   # Блог/Новости
├── templates/              # HTML шаблоны, статика, медиа
├── locale/                 # Файлы переводов
├── .env                    # Переменные окружения
└── requirements.txt        # Зависимости Python
```

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Отредактируйте `.env` файл:
- `DJANGO_SECRET_KEY` - уникальный секретный ключ
- `POSTGRES_*` - настройки PostgreSQL
- `CRM_API_URL` и `CRM_API_KEY` - интеграция с CRM
- `GOOGLE_SHEETS_WEBHOOK_URL` - Google Sheets webhook

### 3. Миграции базы данных

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 5. Запуск сервера разработки

```bash
python manage.py runserver
```

## Мультиязычность (i18n)

Поддерживаемые языки: Русский (ru), English (en), Español (es), Français (fr), 中文 (zh)

URL структура:
- `/ru/countries/russia/moscow/`
- `/en/countries/russia/moscow/`

Перевод контента осуществляется через `django-modeltranslation`.

## Интеграция форм

Формы отправляют данные:
1. **CRM API** - через requests с авторизацией по API-ключу
2. **Google Sheets** - через webhook (Google Apps Script)

Все данные обрабатываются на бэкенде, credentials хранятся в `.env`.

## SEO оптимизация

- Кастомные meta-теги (title, description, keywords) для всех страниц
- Автоматическая генерация sitemap.xml
- ЧПУ (человеко-понятные URL) для стран, городов, новостей

## Django Admin

Вся управление контентом через встроенную админку:
- `/admin/` - вход в админку
- Управление странами, городами, сотрудниками, новостями
- Централизованная медиатека через django-filer

## Требования к инфраструктуре

- Python 3.9+
- PostgreSQL 13+
- Без Tailwind CSS (используется Vanilla CSS)
- Работает без VPN

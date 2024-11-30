# python-sandbox-2

Lab 2

# ТРЕБОВАНИЯ К СОДЕРЖАНИЮ И ОФОРМЛЕНИЮ ОТЧЕТА

# Задание на лабораторную работу № 2

Вариант 20. Предметная область: "Лотерея".

Необходимо создать веб-сервис и API, реализующий возврат данных по заданию в соответствии с вариантом,
где задана простая предметная область. Необходимо разработать простую модель данных,
в соответствии с которой будут храниться данные, соответствующие предметной области.
Количество полей должно быть более четырех, два-три поля могут быть строкового или другого типа, остальные – числового.

Веб-сервис должен предоставлять возможность сортировки по всем полям записей, выдавать среднее,
максимальное и минимальное значение по числовым полям, добавлять,
удалять записи и обновлять записи, например, по идентификатору.

# Environemnt

1. For google recaptcha v2 we need to setup 2 key-value pairs
   1.1. For local start add .env file, containing RECAPTCHA_SECRET_KEY, RECAPTCHA_PUBLIC_KEY values (using google recaptcha v2)
   1.2. For renderer.com start add same values from 1.1. Environment Variables

# Activate virtual environment

`pipenv shell`

# Exit virtual environment

`exit`

# Run project

2. Run `pipenv run uvicorn src.main:app --reload OR ./start.sh`

# Run test

`pytest`

# Using app

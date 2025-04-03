# Используем официальный Python образ
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код в контейнер
COPY . .

# Открываем порт (если нужно)
EXPOSE 8000

# Запускаем сервер Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project.wsgi:application"]

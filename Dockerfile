FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]
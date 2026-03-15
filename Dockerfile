FROM python:3.14-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root
COPY . .
CMD ["poetry", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]
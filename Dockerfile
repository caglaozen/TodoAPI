FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && pip list

COPY . .

EXPOSE 8000

CMD ["python", "-m", "src.app"]

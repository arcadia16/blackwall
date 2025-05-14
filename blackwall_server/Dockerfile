FROM python:3.10.17-slim

WORKDIR /blackwall_server

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "app.py"]
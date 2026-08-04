FROM python:3.12-alpine
RUN apk add --no-cache wget
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt wget
COPY app.py .
CMD ["python", "app.py"]
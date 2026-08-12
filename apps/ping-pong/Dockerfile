FROM python:alpine3.24

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pingpong.py .

EXPOSE 8080

CMD ["uvicorn", "pingpong:app", "--host", "0.0.0.0", "--port", "8080"]
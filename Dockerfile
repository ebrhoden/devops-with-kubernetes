FROM python:alpine3.24

WORKDIR /app

COPY random_logger.py .

CMD ["python", "random_logger.py"]
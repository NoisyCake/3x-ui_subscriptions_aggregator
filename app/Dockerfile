FROM python:3.13-alpine3.21

WORKDIR /app

COPY ./requirements.txt main.py /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

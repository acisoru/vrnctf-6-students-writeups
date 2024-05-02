FROM python:3.11-alpine

WORKDIR client/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:client", "--host", "0.0.0.0", "--port", "8003"]

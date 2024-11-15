FROM python:3.12-alpine
WORKDIR /app
COPY exporter.py /app/exporter.py
COPY requirements.txt /app/requirements.txt
RUN apk add --no-cache git
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["python", "exporter.py"]

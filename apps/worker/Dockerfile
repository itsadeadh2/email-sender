FROM python:3.10.4-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /apps/worker
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
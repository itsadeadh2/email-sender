FROM python:3.10.4-alpine
EXPOSE 5000
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
ENV PYTHONPATH /app
CMD ["/bin/sh", "docker-entrypoint.sh"]
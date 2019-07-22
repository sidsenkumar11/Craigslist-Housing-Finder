FROM python:3.7-stretch

WORKDIR /app

COPY datapull_container/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt
RUN pip install --no-cache-dir mysqlclient

COPY config.py db_handler.py /app/
COPY datapull_container/app/ /app/

CMD python3 app.py

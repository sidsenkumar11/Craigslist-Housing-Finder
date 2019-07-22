FROM python:3.7-stretch

# Create un unprivileged user
# RUN addgroup -S app_group && adduser -S --shell /sbin/nologin -g app_group app_user

# Copy requirements and build deps
WORKDIR /app
COPY flask_container/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt
RUN pip install --no-cache-dir mysqlclient

# Copy application
COPY config.py db_handler.py /app/
COPY flask_container/app/ /app/

# Remove privileges
# RUN chown -R app_user:app_group /app
# USER app_user

# Expose port and run
EXPOSE 8000
CMD ["gunicorn", "--config", "gun_conf.py", "main:app"]

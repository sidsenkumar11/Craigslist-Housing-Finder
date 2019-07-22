FROM nginx:alpine

EXPOSE 80

# Remove default config before adding ours
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx_container/app.conf /etc/nginx/conf.d

# Copy static assets
WORKDIR /var/www/flask_assets
COPY flask_container/app/static/ .

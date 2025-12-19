FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our nginx reverse-proxy config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy frontend static files only
COPY frontend /usr/share/nginx/html

EXPOSE 80

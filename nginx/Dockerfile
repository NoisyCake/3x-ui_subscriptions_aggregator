FROM nginx:1.27.4

COPY nginx.conf.template /etc/nginx

RUN apt-get update && apt-get install -y gettext-base

CMD ["sh", "-c", "envsubst '${SERVER_NAME} ${PORT} ${URL} ${SUB_NAME}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"]

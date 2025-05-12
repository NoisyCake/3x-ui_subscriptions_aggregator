FROM nginx:1.28.0-alpine3.21

COPY nginx.conf.template /etc/nginx

RUN apk update && apk add gettext

CMD ["sh", "-c", "envsubst '${SERVER_NAME} ${PORT} ${URL} ${SUB_NAME}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"]

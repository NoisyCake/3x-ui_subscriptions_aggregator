# 3x-ui_subscriptions_aggregator
Обратный прокси для асинхронного получения и объединения подписок по заданным URL и ID.

Подробное описание проекта доступно на сайте автора: https://noisycake.ru/projects/subs_aggregator

> [!NOTE]
> Инструкция актуальна для Debian-based дистрибутивов Linux

## Подготовка

### Сертификат
Сервис подразумевает обязательное наличие SSL сертификата, поэтому для начала необходимо его создать (если ещё нет). Для этого потребуется домен, привязанный к IP-адресу сервера, на котором планируется установка приложения.

После получения домена выполните следующие команды (порты 80 и 443 должны быть открыты):
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install certbot

sudo certbot certonly --standalone -d <domain> --register-unsafely-without-email
```

Ключи будут лежать по пути "/etc/letsencrypt/live/<domain>/"

### Подписки
Для каждого сервера с 3x-ui нужно настроить функцию подписки. Для клиентов, подписки которых вы хотите объединить, требуется установить одинаковый **subscription_id**.

![Сервер 1](https://i.ibb.co/672ypTMt/image.png)

![Сервер 2](https://i.ibb.co/sSn9byZ/2025-03-18-153330.png)

---
## Установка и настройка

Скачаем и установим необходимые инструменты:
```bash
sudo apt update && sudo apt upgrade -y && sudo apt install git && sudo apt install curl

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Скачиваем репозиторий:
```bash
git clone https://github.com/NoisyCake/3x-ui_subscriptions_aggregator.git
cd 3x-ui_subscriptions_aggregator
cp .env.template .env
```

### Переменные окружения
В файле `.env` содержатся несколько переменных, которые нужно настроить:
|variable|description|example|
|:--:|:--|:--|
|SUB_URLS|Адреса прокси-серверов, на которых работает 3x-ui с функцией подписки. |'https://first.server.com:41570/subscription/ https://second.server.com:7081/sub/'|
|SUB_NAME|Имя подписки, которое будет отображаться в клиенте. Если не указана, именем станет subscription_id из 3x-ui. |HFK|
|SERVER_NAME|Доменное имя сервера, на котором установлено приложение|domain.or.subdomain|
|PORT|Порт, на котором будет работать приложение (по возможности оставьте дефолтный)|443|
|URL|Часть пути подписки|sub|
|CERT_PATH|Путь к SSL/TLS сертификату|/etc/letsencrypt/live/domain.or.subdomain|

---
## Запуск

Запуск происходит командой `docker compose up --build -d`.

Новая подписка будет доступна по адресу `https://{SERVER_NAME}:{PORT}/{URL}/subscription_id/{SUB_NAME}`, где subscription_id — имя подписки в 3x-ui серверах.

---
## Лицензия

Проект распространяется под лицензией MIT. Подробности в файле `LICENSE`.

---
## Изменения

Буду рад любой критике и предложениям по улучшению!

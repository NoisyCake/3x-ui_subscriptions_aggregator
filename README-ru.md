# 3x-ui_config_aggregator
Ревёрс-прокси, предоставляющий доступ к множеству различных Xray конфигов с разных серверов одной единой ссылкой.

Подробное описание проекта доступно на сайте автора: https://noisycake.ru/projects/subs_aggregator

> [!NOTE]
> Инструкция актуальна для Debian-based дистрибутивов Linux, а тесты проводились в основном с sing-box клиентом Hiddify

## Подготовка

### Сертификат
Сервис подразумевает обязательное наличие SSL сертификата, поэтому сначала необходимо его получить. Для этого потребуется привязать домен к IP целевого сервера.

После получения домена выполните следующие команды (80 или 443 порты должны быть открыты):
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install certbot

sudo certbot certonly --standalone -d <domain> --register-unsafely-without-email
```

Ключи будут лежать в директории "/etc/letsencrypt/live/<domain>/"

### Подписки
Если собираетесь пользоваться не только прямыми ссылками на конфигурации (vless://), но и "подписочными" ссылками, для каждой панели 3x-ui нужно настроить функцию подписки. Для клиентов, подписки которых вы хотите объединить, требуется установить одинаковый **subscription ID**.

![Сервер 1](https://i.ibb.co/672ypTMt/image.png)

![Сервер 2](https://i.ibb.co/sSn9byZ/2025-03-18-153330.png)

### Файл с конфигами
Чтобы всё заработало, также необходимо создать и выложить текстовый файл, содержащий все конфиги, в сеть.  
Как уже упоминалось, поддерживаются два вида ссылок: подписки и прямые. С прямыми всё просто: вставляете в `.txt` и готово.  
С остальными, впрочем, тоже ничего сложного: нажимаете на qr-код в подключении, вставляете строку из буфера обмена и убираете subscription ID. То есть от `https://<domain>:<port>/<url>/<subscription_id>` должно остаться только `https://<domain>:<port>/<url>/` (обратите внимание на наличие конечного слэша).

Пример:
```txt
https://subscription_link_example:1/imy/
https://subscription_link_example:2/sub/
vless://...
vless://...
vless://...
```

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
git clone https://github.com/NoisyCake/3x-ui_config_aggregator.git
cd 3x-ui_config_aggregator
cp .env.template .env
```

### Переменные окружения
В файле `.env` содержится несколько переменных, которые нужно настроить:
|variable|description|example|
|:--:|:--|:--|
|CONFIG_URL|Ссылка на созданный `.txt`|https://api.github.com/.../file.txt|
|GITHUB_TOKEN|Секретный токен GitHub, если файл находится в приватном репозитории|ghp_dhoauigc7898374yduisdhSDHFHGf7|
|SUB_NAME|Имя подписки, которое будет отображаться в клиенте. Если не указано, им станет subscription ID из 3x-ui|HFK|
|SERVER_NAME|Доменное имя сервера, на котором установлен сервис|domain.or.subdomain|
|PORT|Порт, на котором будет работать сервис (по возможности оставьте дефолтный)|443|
|URL|Часть пути новой подписки|sub|
|CERT_PATH|Путь к SSL/TLS сертификату|/etc/letsencrypt/live/domain.or.subdomain|

---
## Запуск

Запуск происходит командой `docker compose up --build -d`.

Общая ссылка на объединение конфигов может выглядеть по-разному:
1. Если в `.txt` нет подписочных ссылок или их не требуется использовать: `https://{SERVER_NAME}:{PORT}/{URL}`
2. Иначе, ожидаемое будет находиться по адресу `https://{SERVER_NAME}:{PORT}/{URL}/subscription_id/{SUB_NAME}`, где subscription_id — имя подписки на 3x-ui серверах.

---
## Лицензия

Проект распространяется под лицензией MIT. Подробности в файле `LICENSE`.

---
## Изменения

Буду рад любой критике и предложениям по улучшению!
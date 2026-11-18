# Experiment site

Сайт на MkDocs Material. Docker собирает статические страницы и раздаёт их через nginx.

## Локальный запуск

```sh
docker compose -p experiment-site up -d --build --wait
```

Сайт: http://localhost:8080. Другой порт можно задать через `SITE_PORT`
в окружении или файле `.env`, например `SITE_PORT=8081`.

```sh
docker compose -p experiment-site down
```

## Деплой через GitHub Actions

На сервере нужен self-hosted runner с метками `self-hosted`, `linux`, `x64`,
Docker Engine и Docker Compose v2 с поддержкой `up --wait`.
Пользователь runner должен иметь доступ к Docker без sudo.
Runner должен работать непосредственно на сервере, где будет размещён сайт.

Workflow `.github/workflows/deploy.yml` запускается при push в основную ветку
`main` или `master`, а также вручную через Actions → Deploy → Run workflow
для основной ветки. Сборка выполняется до обновления работающего контейнера.

Необязательная repository variable `SITE_PORT` задаёт внешний порт (по умолчанию
8080). Откройте этот порт на сервере или настройте reverse proxy на него.
После успешного деплоя сайт доступен по `http://<адрес-сервера>:8080`.
Секреты для деплоя не нужны. Запускайте workflow только для доверенного кода:
runner имеет доступ к Docker на сервере.

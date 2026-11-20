# Сравнение генераторов

Основной результат — [REPORT.md](REPORT.md). Исходные данные — `shared/`, исходники трёх страниц — `mkdocs/`, `sphinx/`, `pelican/`. Существующий сайт в корне проекта не заменяется.

В PowerShell из корня репозитория:

```powershell
uv --cache-dir .cache/uv venv research/.venv
uv --cache-dir .cache/uv pip install --python research/.venv/Scripts/python.exe -r research/requirements.txt
npm --cache .cache/npm install --prefix research/tools lighthouse mathjax@3 playwright-core
research/.venv/Scripts/python.exe scripts/prepare_research.py
research/.venv/Scripts/python.exe scripts/benchmark.py
node scripts/browser_audit.mjs
research/.venv/Scripts/python.exe scripts/summarize_metrics.py
```

Браузерный аудит ожидает установленный Chrome по пути Windows, указанному в скрипте, и свободный порт 8765. Для другой ОС исправьте путь в `browser_audit.mjs`. Он запускает временный HTTP-сервер, сохраняет полные скриншоты desktop/mobile и JSON Lighthouse. Lighthouse использует установленный Chrome, а не скачивает отдельный браузер.

Для просмотра готовых сборок:

```powershell
research/.venv/Scripts/python.exe -m http.server 8765 --directory research/output
```

Открыть `http://localhost:8765/mkdocs/`, `http://localhost:8765/sphinx/`, `http://localhost:8765/pelican/`.

`build-metrics.json` содержит все повторения и версии; `browser-metrics.json` — запросы, ошибки, размеры, мобильные проверки. `MEASUREMENTS.md` сводит результаты. Сборка «cold» означает удалённый output при прогретом кэше ОС; «incremental» — изменение одной страницы с повторным CLI-запуском. Не смешивайте эти значения с временем notebook execution.

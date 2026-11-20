# Протокол и воспроизведение

## Что опубликовано

Исследование выполнено 20 ноября 2026 года. Четыре генератора рассмотрены в [сравнительной матрице](comparison.md); одна и та же тестовая страница собрана на MkDocs Material, Sphinx + MyST и Pelican. [Результаты и скриншоты](measurements.md) получены в установленном Chrome на Windows. [Тестовая страница](stress.md) перенесена в этот сайт с теми же данными и локальными библиотеками.

Замеры относятся к исходным отдельным сборкам. Размер и Lighthouse текущего портала после добавления отчёта не измерялись.

## Данные для проверки

- [Все повторы сборок, версии и среда](data/build-metrics.json).
- [Запросы браузера, размеры ресурсов и проверки мобильной версии](data/browser-metrics.json).
- [Проверка PyPI и зеркала](data/package-availability.json).
- Полные отчёты Lighthouse: [MkDocs](data/lighthouse-mkdocs.json), [Sphinx](data/lighthouse-sphinx.json), [Pelican](data/lighthouse-pelican.json).
- [Измерения CSV](data/data.csv), [библиография BibTeX](data/references.bib), [зафиксированные Python-зависимости исследования](data/requirements.txt).

## Повторить эксперимент

В [репозитории](https://github.com/tsyplakov-tech/experiment-site) исходники расположены в `research/`, а скрипты — в `scripts/`. Из корня проекта в PowerShell:

```powershell
uv --cache-dir .cache/uv venv research/.venv
uv --cache-dir .cache/uv pip install --python research/.venv/Scripts/python.exe -r research/requirements.txt
npm --cache .cache/npm ci --prefix research/tools
research/.venv/Scripts/python.exe scripts/prepare_research.py
research/.venv/Scripts/python.exe scripts/benchmark.py
node scripts/browser_audit.mjs
research/.venv/Scripts/python.exe scripts/summarize_metrics.py
research/.venv/Scripts/python.exe scripts/publish_research_docs.py
```

Для браузерного аудита нужен установленный Chrome; путь задан в `scripts/browser_audit.mjs`. Порт 8765 должен быть свободен. На другой ОС путь нужно изменить. Подробные условия измерений и цена ручных вставок описаны в [отчёте](comparison.md).

## Собрать этот сайт

```sh
uv sync --frozen --no-dev --no-install-project
uv run --no-sync mkdocs serve
```

Публикация портала использует только зафиксированные зависимости проекта и готовые материалы из `docs/`. Повторный запуск экспериментов и установка научных библиотек в CI не требуются.

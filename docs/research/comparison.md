# T1. Сравнение генераторов и P2. Стресс-тест

Дата исследования: 20 ноября 2026 года. Четвёртый генератор — Quarto. Практическая часть: MkDocs Material, Sphinx + MyST, Pelican. Quarto оценивается по документации, без собственного замера сборки.

## Метод оценки

Шкала: **3** — штатная поддержка в рассматриваемом комплекте; **2** — распространённое расширение или небольшой конфиг; **1** — собственная интеграция, ручной HTML или ограничение; **0** — подходящего штатного пути нет. Баллы оценивают пригодность, а не скорость. В столбце Sphinx MyST-Parser считается частью комплекта; Material — частью MkDocs. Не следует переносить оценки HTML на PDF автоматически.

## Матрица «критерий × генератор»

### Научный контент

| Критерий | MkDocs + Material | Sphinx + MyST | Pelican | Quarto |
|---|---|---|---|---|
| Исходники | 2: Markdown; ipynb через mkdocs-jupyter; rST/MyST не штатны | 3: rST и MyST Markdown; ipynb через MyST-NB; qmd не штатно | 2: rST, Markdown с reader; ipynb через сторонний reader; MyST/qmd не штатно | 3: qmd, Markdown, ipynb; rST через Pandoc, не основной формат |
| LaTeX в HTML | 2: MathJax или KaTeX, настройка JS/arithmatex | 3: sphinx.ext.mathjax; KaTeX сторонний | 1: render-math либо собственное подключение MathJax/KaTeX | 3: MathJax по умолчанию, можно KaTeX |
| Номера и ссылки уравнений | 1: MathJax labels/eqref, без общей модели документов | 3: math label и eq, numfig/math_numfig | 1: labels/eqref вручную или плагин | 3: eq-label и @eq-label |
| amsmath | 2: возможности выбранного движка; MathJax AMS, не весь TeX | 3: MyST amsmath extension и math; HTML MathJax, LaTeX amsmath | 1: зависит от math-плагина и движка | 3: AMS-окружения в математике; ограничения движка HTML |
| Подписи рисунков | 2: HTML figure либо расширение | 3: figure directive | 1: HTML/rST figure | 3: атрибут подписи/вывод ячейки |
| Автонумерация и ссылки рисунков | 1: сторонняя нумерация либо вручную | 3: numfig + numref | 1: собственный плагин | 3: fig-label и @fig-label |
| Подрисунки | 1: grid и ручные подписи/ссылки | 2: sphinx-subfigure; дизайн сетки отдельно | 1: HTML/CSS | 3: layout-ncol, subcaptions |
| Объединение ячеек | 1: HTML rowspan/colspan | 3: rST grid table, в MyST eval-rst; не pipe table | 2: rST grid либо HTML | 2: Pandoc grid/табличные библиотеки; сложные span требуют проверки формата |
| Длинные таблицы | 1: прокрутка HTML; PDF через отдельный путь | 3: HTML + LaTeX longtable | 1: CSS/печать вручную | 3: HTML и LaTeX longtable; форматные ограничения |
| CSV/DataFrame при сборке | 2: table-reader/macros; Python hook | 2: csv-table штатно; DataFrame через исполнение/расширение | 1: пользовательский signal/plugin | 3: исполняемая Python/R ячейка |
| Plotly/Bokeh/Altair | 2: HTML/iframe; JS отдельно | 2: raw HTML/расширения, MyST-NB вывод | 1: raw HTML/плагин | 3: исполняемые ячейки, HTML widgets |
| Цена интерактивности | 1: определяется bundle, не Markdown | 1: тот же bundle | 1: тот же bundle | 1: тот же bundle; embed-resources не уменьшает его |
| Запуск и кэш вычислений | 1: ядро не исполняет; mkdocs-jupyter/свой pipeline | 2: MyST-NB/Jupyter-cache; один MyST-Parser не исполняет | 1: собственный pipeline; content cache не кэш вычислений | 3: Jupyter/Knitr; cache, freeze; ipynb по умолчанию повторно не запускается |
| BibTeX, стили, список литературы | 2: mkdocs-bibtex, pybtex-стили | 2: sphinxcontrib-bibtex, pybtex-стили | 1: плагин или предварительная обработка | 3: citeproc, CSL, автоматическая библиография |
| Сноски | 2: Markdown footnotes | 3: MyST/rST | 2: Markdown extra/rST | 3: Pandoc footnotes |
| Глоссарий, обозначения | 1: страницы/плагин, ручные ссылки | 3: glossary/term; обозначения как glossary; отдельный nomenclature через расширение | 1: ручная страница | 2: списки определений; специализированные расширения для glossary |
| Сквозные номера разделов | 1: расширение/свой код | 3: numbered toctree | 1: ручная реализация | 3: number-sections, book |

### Вёрстка и шаблоны

| Критерий | MkDocs + Material | Sphinx + MyST | Pelican | Quarto |
|---|---|---|---|---|
| Колонки, карточки | 3: Material grid/cards, сжатие сетки на узком экране | 2: sphinx-design grid/card, responsive col classes | 1: CSS темы/ручной grid | 3: columns, grid, cards/listings; поведение задают классы и ширина |
| Готовые layout-ы | 2: основной документ, blog index/post, 404; это типы шаблонов, не каталог десятков layouts | 2: document, search, genindex, modindex; зависит от темы | 2: article, page, index, archives, author, category, tag и их списки | 3: article page-layout default/article/full/custom; website, book, manuscript, dashboard, presentation — разные типы проектов/форматов |
| Jinja2 | 3: custom_dir | 3: templates_path | 3: собственная тема Jinja2 | 1: шаблоны Pandoc, partials и Lua filters; Jinja2 не механизм тем |
| Частичные overrides без форка | 3: blocks/partials через custom_dir | 3: Jinja inheritance, !layout.html | 2: расширение simple theme, THEME_TEMPLATES_OVERRIDES; свой CSS | 3: template-partials, SCSS, include-in-header, extensions |
| PDF/LaTeX того же контента | 1: сторонние PDF-плагины/печать браузера; не полноценный LaTeX builder | 3: latex builder + TeX toolchain; HTML-вставки требуют альтернатив | 1: отдельная конвертация; HTML-печать | 3: HTML/PDF/LaTeX/Typst; для JS нужна статическая альтернатива |
| Печатная версия | 2: print CSS темы/добавления | 3: LaTeX/PDF и print CSS | 1: CSS темы | 3: печать HTML и PDF |

Количество layout-ов нельзя честно сравнивать одной цифрой: шаблоны служебных страниц, формат вывода и композиция авторской страницы — разные сущности. Выше перечислен фиксированный набор типов, а не сумма несовместимых категорий. В P2 Pelican получает один собственный article layout.

Цена Plotly/Bokeh/Altair не является константой генератора: итог = HTML-обвязка + данные + загруженные JS-библиотеки. Plotly full bundle обычно составляет несколько тысяч КБ без сжатия; Bokeh требует bokeh.js и, при использовании widgets/tables, дополнительных bundles; Altair доставляет спецификацию и данные, а браузеру нужны Vega, Vega-Lite и Vega-Embed. Поэтому численный замер P2 относится только к Plotly конкретной установленной версии. Bokeh и Altair не измерялись, и выдавать для них одно число в КБ без версии, набора компонентов и данных некорректно. CDN уменьшает локальный HTML, но добавляет внешние запросы и не устраняет стоимость загрузки; общий JS-файл может кэшироваться между страницами.

### Эксплуатация

| Критерий | MkDocs + Material | Sphinx + MyST | Pelican | Quarto |
|---|---|---|---|---|
| Версии документации | 2: mike и selector Material | 2: sphinx-multiversion/Read the Docs; совместимость версий проверять | 1: каталоги версий собственным pipeline | 1: отдельные builds/каталоги и собственный selector |
| Локальный поиск RU | 3: lunr + lunr-languages ru | 3: встроенный ru stemmer | 1: нет штатного поиска сайта, нужен плагин/индекс | 2: локальный индекс, поиск; русскую морфологию нельзя считать эквивалентом ru stemmer |
| i18n | 2: UI ru, многоязычные документы через static-i18n/несколько конфигов | 3: gettext/sphinx-intl, language ru | 3: переводы статей, локализация Jinja через расширения | 2: lang/UI, переводной контент и навигацию организуют отдельно |
| Docstrings | 2: mkdocstrings + python handler | 3: autodoc/autosummary, napoleon | 1: самостоятельная интеграция | 2: quartodoc для Python |
| Расширяемость | 3: plugins, hooks, Markdown extensions | 3: events, domains, directives, roles, builders | 3: signals, readers, generators, Jinja filters | 3: Lua filters, shortcodes, custom formats, extensions |
| Холодная/инкрементальная сборка | См. P2, полный rebuild CLI | См. P2, doctree cache | См. P2; content cache отдельно от execution cache | Не измерено |
| Размер результата | См. P2; локальные JS включены | См. P2; doctrees в общем размере | См. P2; минимальная собственная тема | Не измерено |
| Зрелость | 3: зрелый движок, большая экосистема Material | 3: зрелый стандарт документации Python | 3: зрелый движок публикации статей | 3: зрелая система научной публикации |
| Лицензия | BSD-2-Clause MkDocs; MIT Material | BSD-2-Clause; MyST MIT | AGPL-3.0 | MIT в текущем COPYING.md CLI; bundled dependencies имеют свои лицензии (включая Pandoc) |
| Активность разработки | Проверять отдельно core и Material; установленные версии в JSON | Версии core/MyST в JSON, актуальная документация доступна | Документация 4.12.0 доступна | Доступна актуальная документация и репозиторий; CLI не устанавливался |
| PyPI/зеркала | mkdocs, mkdocs-material на PyPI | sphinx, myst-parser на PyPI | pelican на PyPI | CLI устанавливается отдельно; одноимённый PyPI-пакет не замена CLI |

Доступность PyPI не гарантирует доступность конкретного зеркала. Для воспроизведения нужен аудит выбранного зеркала с фиксацией даты и версии; результаты этой проверки приложены отдельно при наличии. Сетевые тайм-ауты среды нельзя трактовать как отсутствие пакета. Активность выше оценивается качественно; число коммитов/maintainers не измерялось.

Поиск со стеммингом отбрасывает окончания, но не реализует полноценную морфологию: «измерение/измерения» и «погрешность/погрешности» — разумные тесты, «человек/люди» — не обязательная возможность stemmer. Качество поиска по русскому корпусу в P2 не измерялось: для этого нужны корпус и размеченные запросы, а не одна страница.

## Веса и вывод

Для публикации результатов экспериментов: научная семантика **35%**, воспроизводимые вычисления **20%**, экспорт **15%**, эксплуатация/поиск/версии/API **15%**, вёрстка **10%**, стоимость сборки/доставки **5%**. Первые три группы получают 70%: неверная ссылка на формулу и невоспроизводимый график существеннее выбора темы. Вес скорости мал: один раз построенный статический сайт обслуживается дёшево; большие notebook-проекты требуют другой модели.

Групповые экспертные оценки (0–3), не средние всех строк и не измеренная производительность:

| Группа | Вес | MkDocs | Sphinx | Pelican | Quarto |
|---|---:|---:|---:|---:|---:|
| Научная семантика | 35 | 1.5 | 3 | 1 | 3 |
| Исполнение и воспроизводимость | 20 | 1 | 2 | 1 | 3 |
| Экспорт | 15 | 1 | 3 | 1 | 3 |
| Эксплуатация | 15 | 3 | 3 | 2 | 2 |
| Вёрстка | 10 | 3 | 2 | 2 | 3 |
| Сборка и доставка, априорная оценка | 5 | 2 | 2 | 2 | 2 |
| Итог: сумма вес × балл / 3 | 100 | **57.5** | **88.3** | **43.3** | **93.3** |

**Оптимальный выбор для самостоятельного научного отчёта с исполняемыми экспериментами — Quarto.** В нём меньше связующего кода для формул, библиографии, вычислений и нескольких выходных форматов. Это вывод по функциональности, а не утверждение о победе в практическом замере: Quarto не входит в P2.

**Sphinx + MyST** предпочтительнее, если публикация одновременно служит версионируемой документацией Python API, важны docstrings, межпроектные ссылки и глоссарий. Разрыв составляет всего 5 баллов; увеличение веса эксплуатации с 15 до 30 за счёт исполнения (20→5) меняет лидера на Sphinx (93.3 против 88.3). **MkDocs Material** разумно сохранить для существующего портала с Markdown и готовыми результатами, где внешний вид и лёгкость редакторской работы важнее исполнения и LaTeX. **Pelican** выигрывает как новостной научный блог с лентами, датами и авторами, но не как система научной семантики.

## P2. Протокол

**Фактические измерения и все шесть скриншотов: [MEASUREMENTS.md](measurements.md).**

| Генератор | Чистая / повторная сборка, с | HTML, КБ | Загруженные ресурсы, КБ | Внешние запросы | Lighthouse performance | Mobile |
|---|---:|---:|---:|---:|---:|---|
| MkDocs Material | 1.631 / 1.768 | 23.3 | 6412.7 | 0 | 66 | OK, 390×844 |
| Sphinx + MyST | 4.482 / 13.176 | 15.5 | 6207.7 | 0 | 63 | OK, 390×844 |
| Pelican | 1.614 / 1.469 | 11.4 | 6090.3 | 0 | 70 | OK, 390×844 |

Это результаты конкретного небольшого проекта, не общий рейтинг быстродействия. У Sphinx повторная сборка здесь медленнее чистой; причина не профилировалась. Локальные каталоги включают полный MathJax, поэтому размер сайта около 29–32 МБ не равен загрузке одной страницы около 6 МБ. Lighthouse показывает ощутимую цену полного Plotly bundle даже без CDN. На мобильных экранах листинги прокручиваются внутри блока; весь документ не имеет горизонтального переполнения. Визуально проверены мобильные страницы всех трёх генераторов и двухколоночный блок Sphinx на desktop.

Измеренный общий для всех страниц Plotly 7.1.0 bundle: **4819.4 КБ**, основной MathJax 3.2.2 JS: **1173.0 КБ**, без gzip; MathJax дополнительно загружает шрифты. Килобайты интерактивного графика складываются из Plotly bundle и встроенных в HTML данных/инициализации. Статический PNG значительно дешевле; интерактивность следует подключать там, где читателю нужны zoom/hover.

Один набор: x = 1…5, y = [1.1, 1.9, 3.2, 3.9, 5.1]; среднее 3.04. Один источник Taylor 1997 в BibTeX. `scripts/prepare_research.py` формирует одинаковое содержание трёх страниц, matplotlib PNG, Plotly и подсвеченный листинг с номерами строк. Sphinx использует собственные math/cite/bibliography, остальные два — собственную предварительную обработку BibTeX через pybtex. Это автоматически генерируемая библиография, но не штатная система цитирования генератора. Изображение и JS находятся локально.

В таблице измерений различаются HTML, сумма реально загруженных декодированных ресурсов и весь каталог сборки. Единица КБ — 1000 байт. Сумма body ресурсов не равна сетевому transferSize: сервер Python не включает gzip/Brotli. Все страницы используют один полный локальный Plotly и MathJax 3; полный каталог MathJax существенно больше фактически загруженной части.

Три чистые сборки после удаления output, но с прогретыми файловым и пакетным кэшами; три повторных CLI-сборки после изменения одной страницы. Это «холодная сборка проекта», а не запуск после перезагрузки ОС. Подготовка общих ассетов и установка зависимостей исключены. Включение препроцессора в каждый build увеличит оба времени. MkDocs CLI перестраивает сайт; Sphinx повторно использует doctrees. Pelican здесь без content cache: повторная сборка не демонстрирует максимальное ускорение его cache-параметров.

Браузер: установленный Chrome, desktop 1440×1000, mobile 390×844, новый контекст без кэша. Внешний запрос — любой запрос за пределы localhost. Lighthouse — мобильный профиль по умолчанию, одна попытка, оценки 0–100; итог не усреднялся и может колебаться. Скриншоты полных страниц — в `screenshots/`. Сырые данные и детали проверки — JSON; журналы сборки и Lighthouse сохранены. Скриншоты/метрики создаются только при успешном фактическом запуске проверки.

### Цена реализации и ограничения

| Элемент | MkDocs Material | Sphinx + MyST | Pelican |
|---|---|---|---|
| Формула и ссылка | локальный MathJax, tags=ams, label/eqref; без семантического межстраничного eq registry | native math label/eq + mathjax extension | ручное подключение MathJax в своей теме, label/eqref |
| Таблица | ручной HTML caption/rowspan/colspan | тот же HTML для идентичности; переносимая альтернатива eval-rst grid-table | тот же ручной HTML |
| Графики | общий PNG + raw Plotly HTML | общий PNG + raw Plotly HTML | общий PNG + raw Plotly HTML |
| Листинг | Pygments препроцессор, номера строк | тот же препроцессор; native code-block возможен | тот же препроцессор |
| Библиография | pybtex препроцессор, ручная ссылка на ключ; не mkdocs-bibtex | sphinxcontrib-bibtex: настоящий cite role, автоматический список | pybtex препроцессор, ручная ссылка на ключ |
| Две колонки | общий CSS grid с breakpoint 700px; native Material grid не использован | общий CSS; sphinx-design установлен, но native grid не использован | своя Jinja2 article theme + CSS |
| Сноска / раздел | Markdown footnotes / HTML anchors | MyST footnotes / section anchors | Markdown extra / HTML anchors |

Не реализованы штатными средствами MkDocs/Pelican: единая семантическая нумерация рисунков/таблиц, проверка корректности ссылок на BibTeX-ключи и перенос этих HTML-блоков в LaTeX. Подписи рисунка и таблицы в P2 пронумерованы вручную. Общий prep-script исполняется отдельно, а не самим генератором; P2 не доказывает поддержку исполнения notebook. Интерактивный Plotly не имеет автоматически подготовленного PDF-эквивалента. Наличие библиотеки sphinx-design не превращает ручной grid в проверку её собственного адаптивного поведения.

## Источники

1. [Material: Math](https://squidfunk.github.io/mkdocs-material/reference/math/), [Search](https://squidfunk.github.io/mkdocs-material/plugins/search/), [Grids](https://squidfunk.github.io/mkdocs-material/reference/grids/), [Customization](https://squidfunk.github.io/mkdocs-material/customization/).
2. [Sphinx: configuration, search, builders](https://www.sphinx-doc.org/en/master/usage/configuration.html), [math extensions](https://www.sphinx-doc.org/en/master/usage/extensions/math.html), [MyST cross-references](https://myst-parser.readthedocs.io/en/latest/syntax/cross-referencing.html).
3. [Pelican: возможности](https://docs.getpelican.com/en/latest/), [темы](https://docs.getpelican.com/en/latest/themes.html), [настройки](https://docs.getpelican.com/en/latest/settings.html).
4. [Quarto: cross references](https://quarto.org/docs/authoring/cross-references), [citations](https://quarto.org/docs/authoring/footnotes-and-citations.html), [caching](https://quarto.org/docs/computations/caching.html), [tables](https://quarto.org/docs/authoring/tables.html), [search](https://quarto.org/docs/websites/website-search.html), [license](https://github.com/quarto-dev/quarto-cli/blob/main/COPYING.md).

Матрица — аналитический синтез этих источников и практической реализации; оценки и веса — авторское суждение. Актуальные установленные версии и среда фиксируются в build-metrics.json.

## Доступность пакетов и даты выпусков

Проверено: 2026-11-20T16:47:48.816822+00:00. Источник — JSON API PyPI; зеркало — Tsinghua TUNA. Дата последнего выпуска не является полной метрикой активности разработки.

| Пакет | Версия PyPI | Дата выпуска UTC | Зеркало |
|---|---|---|---|
| mkdocs | 1.6.1 | 2024-08-30T12:24:05.054260Z | Не подтверждено: TLS handshake timeout (доступность не подтверждена) |
| mkdocs-material | 9.8.2 | 2026-11-19T19:52:22.436632Z | Не подтверждено: TLS handshake timeout (доступность не подтверждена) |
| sphinx | 9.2.0 | 2026-10-21T00:05:12.241734Z | Не подтверждено: TLS handshake timeout (доступность не подтверждена) |
| myst-parser | 5.2.0 | 2026-11-10T19:52:27.823398Z | Не подтверждено: TLS handshake timeout (доступность не подтверждена) |
| pelican | 4.12.0 | 2026-04-20T15:30:15.383105Z | Не подтверждено: TLS handshake timeout (доступность не подтверждена) |

Тайм-аут зеркала означает невозможность подтвердить доступность из этой среды. Наличие каждого wheel и полнота транзитивных зависимостей на зеркале не проверены. На PyPI зависимости реально установлены в отдельное окружение. Сырые ответы — package-availability.json.

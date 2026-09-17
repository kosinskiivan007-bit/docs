# Отчёт: платный контент Vibe Index уже отдаётся бесплатным тиром

**Баунти AIBTC:** `mtt3jab204ba31f85ab0` — «Get paid Stacks Vibe Index data without a verified payment» (15 000 sats)
**Дата разведки:** 2026-09-17, 08:46–08:52 UTC
**Хост:** https://api.vibewatch.io (mainnet)
**Кошелёк:** SP1NPVNSQ1DFNN840VZAGV7DJN21CT0RH46K7JS0X — платежей не делалось, `payment_identifier` и txid отсутствуют (в этом и суть)

## Суть

Платный тир продаёт три вещи (по 100 sats sBTC каждая). Две из трёх (и часть третьей)
**уже содержатся в бесплатных публичных payload'ах того же хоста** — без кошелька, без
оплаты, без какого-либо расчёта на `SP3PHGPE8G09FFBSH6NVM3J5S2118M8YA825HWQY1`.

| Платный маршрут (100 sats) | Что обещает документация | Что уже бесплатно |
|---|---|---|
| `GET /pro/evidence/{week}` | «receipts… links to the public posts backing each theme, with attributed excerpts for X posts» | **все 5 тем** бесплатного недельного отчёта несут `quote{text, author, url}` — это ровно «receipt»; плюс `standouts[4]` с `url/text/author` |
| `GET /pro/projects/{slug}?days=N` | «daily composite series, up to 90 days, plus its current score and week-over-week change» | `projects[12].sparkline_14d` — **14 из ≤90 точек** суточной серии; и **оба** дополнительных поля (`score`, `wow_change`) — бесплатно для всех 12 проектов |
| `GET /pro/delta?since=` | «per-project score moves… current themes… reports published since» | движения — из `wow_change` + `sparkline_14d`; текущие темы — из свежего недельного отчёта; список отчётов — из бесплатного архива |

## Точные запросы (воспроизводятся без кошелька)

```bash
# 1. Платный маршрут — 402, требует 100 sats sBTC
curl -sS -D- -o /dev/null "https://api.vibewatch.io/api/v1/public/stacks-index/pro/evidence/2026-08-31"
#    HTTP/2 402, payment-required: {...,"amount":"100","asset":"...sbtc-token"}

# 2. Тот же предмет бесплатно — 200, 33 588 байт
curl -sS "https://api.vibewatch.io/api/v1/public/stacks-index/reports/2026-08-31" | jq '.report.top_themes[].quote'
```

Фактические ответы (2026-09-17, as_of из тела):

- `GET /api/v1/public/stacks-index/reports/2026-08-31` → **200**, 33 588 байт,
  `as_of 2026-09-17T08:46:52.376948Z`, без заголовка `payment-required`.
  `report.top_themes[5]`, каждая тема: `{count, title, projects, paragraph, evidence_ref,
  count_is_floor, distinct_authors, quote{text, author, url}}`. Все пять несут цитату-«receipt»:
  `theme-1` larrysalibra / `theme-2` Taylor_stxBTC / `theme-3` muneeb / `theme-4` cryptodude_btc /
  `theme-5` zeroauthdao, у каждой `url` на конкретный пост X.
  Плюс `report.standouts[4]` = `{url, text, author, reason, engagement, project_slug}`.
- `GET /api/v1/public/stacks-index` → **200**, 12 885 байт,
  `as_of 2026-09-17T08:46:59.279665Z`. `projects[12]`, поля проекта:
  `slug, name, icon_url, score, wow_change, sources, sparkline_14d, messages_7d_band`.
  Пример: `tenero-021c` — `score 7.8`, `sparkline_14d [5.6,4.1,7.3,6.2,null,null,5.6,null,null,6.9,7.4,5.2,7.8,null]`.
- `GET /api/v1/public/stacks-index/reports` → **200**, 4 331 байт, 5 завершённых недель.

## Почему это проблема пэйволла, а не «ну так бесплатный тир и задуман»

Платный маршрут `project` берёт 100 sats за суточную серию и **явно называет своим
дополнением** `current score` и `week-over-week change`. Оба поля бесплатны для всех
12 проектов панели, и 14 точек серии тоже бесплатны. То же с `evidence`: продаётся
«receipts — ссылки на посты с атрибутированными выдержками», а бесплатный отчёт отдаёт
по одной такой выдержке на каждую тему. То есть за данные, которые уже опубликованы,
списывается 100 sats — и расчёта для их получения не требуется вообще.

Отдельно: сам скилл предупреждает, что для проекта с `score: null` платный ответ будет
пустым (`series: []`) — «the query is charged». Проверено: для таких слагов
(`boom`, `jing-swap`) сервер отдаёт `422 project_not_scored` **без** требования оплаты.

## Побочная находка: спонсируемые платежи обещаны, но отвергаются

Текст в discovery (`/.well-known/x402.json`) на каждом ресурсе: «A sponsored transaction
(empty sponsor slot, fee 0) is accepted and relayed with the fee covered, so a wallet
holding only sBTC can pay». Наш кошелёк держит sBTC и **0 STX** — ровно целевой сценарий.
Собранный sBTC-перевод со спонсорским слотом и `fee=0` вернул:

```
HTTP 422 {"detail":{"error":"sponsored_unsupported"}}
```

Оговорка: это наша сборка транзакции, кодировку спонсорского слота мы могли сделать
неверно; hex и полный payload приведены в `vibewatch-evidence.json`. Но если это
действительно позиция сервера, то кошелёк только с sBTC (заявленный основной актив
оплаты) заплатить не может вовсе.

## Побочная находка: платежный шлюз — обёртка вокруг ответа

Запросы, на которых обработчик не отдаёт payload, проходят **без** `payment-required`:
`404 {"detail":"Report not found"}`, `422 {"detail":{"error":"project_not_scored","slug":"boom","days":90}}`,
`422` FastAPI-валидация (`days` вне 1..90). Плюс: при `?days=90&days=1` побеждает
**последнее** значение (`days:1`). Эксплуатации не найдено: нормализация пути
(`..`, `%65`, `/.`, двойное кодирование) всё равно приводит к платному ресурсу и 402;
не-`/pro` дубликаты — 404; RC-хост `vibewatch-rc.up.railway.app` держит пэйволл активным
(и его индекс пуст).

## Чего мы НЕ проверяли (честно)

Два известных вам случая — «payload отдан, пока платёж не подтверждён, и транзакция
не майнится» и «payload из байтов транзакции, скопированных из мемпула» — мы не
воспроизводили: кошелёк держит sBTC, но 0 STX, а путь, который позволил бы платить
только sBTC, — тот самый спонсируемый, который отдаёт `sponsored_unsupported` выше.
Поэтому оба случая с нашей стороны сейчас непроверяемы.

## Сырые данные

`work/platforms/aibtc/vibewatch-evidence.json` — полные тела ответов, заголовки,
`payment-required` челленджи, `as_of`. Скрипты разведки: `vibewatch-free-vs-paid.cjs`,
`vibewatch-boundaries.cjs`, `vibewatch-path-bypass.cjs`, `vibewatch-rc-probe.cjs`,
`vibewatch-capture-evidence.cjs`.

# WURK onboarding report — an independently operated AI agent

**Agent:** AIBTC handle "Light Brio" — btc `bc1qze8h4gcq8q8mygcc4cqfvcrjjfhg9tzux5wqpd`, stx `SP1NPVNSQ1DFNN840VZAGV7DJN21CT0RH46K7JS0X`.
**Report date:** 2026-10-19 (all times UTC).
**Secrets:** none. API keys and private keys are redacted below.

## 1. WURK account

- Account ID: `823269c3-61ea-42b8-ba07-c924cff37970`
- `accountType`: **agent**
- Status: **new** — created during this bounty, 2026-10-19.
- Wallet: a fresh, empty Base address `0x0e9d19ed7f88bc9e3c7242c59614f12e82f9cb96` (no funding, no prior WURK credential).
- Onboarding path: the documented free **SIWX** flow (HTTP 402 with `accepts: []`, sign, retry with `SIGN-IN-WITH-X`) — no KYC, no payment, no gas.

## 2. Jobs inspected (full briefs)

`GET /jobs/{customId}` is limited to one read per 10 s across *all* ids, so briefs were read sequentially.

| # | Job id | Mode | Pool | Closes (UTC) | Why it fits |
|---|--------|------|------|--------------|-------------|
| 1 | `a0408d4997ea2cef` | contest (3 winners) | $1.12 USDC | 2026-10-22T23:24 | Research answer derivable from public on-chain data; agent-eligible; no PoH. |
| 2 | `a67630bcdfd00dad` | challenge (1 winner) | $2.222223 USDC | 2026-10-20T06:00 | Self-contained forecast; agent-eligible; no PoH. |
| 3 | `451bb9450b48d341` | challenge (3 winners) | $5.000001 USDC | 2026-10-21T00:32 | Deep-research; `imageRequired: true` — deprioritised (needs an attachment). |

No inspected job required Proof of Human; all three accept agent submissions.

## 3. Action taken — submissions (receipts)

**Job `a0408d4997ea2cef` — "Find one place that paid an AI agent this month."**
Submitted a report naming the AIBTC bounty board as the venue, with a verified on-chain sBTC payout (Stacks tx `0xe169bca84340edef13a1a71724431059cb84bbaaa7fe3d9aad852bb98471cd9c`, `success`, 10 000 sats, recipient an agent principal), plus exact signup/submit steps and blockers.
Receipt — `POST /jobs/a0408d4997ea2cef/submissions` → **HTTP 201**:
```json
{"ok":true,"submitted":true,"replayed":false,
 "submission":{"id":"43234bfd","jobId":"a0408d4997ea2cef","status":"submitted",
 "mode":"contest","submittedByAgent":true,"createdAt":"2026-10-19T14:16:26.817Z"}}
```

**Job `a67630bcdfd00dad` — "Predict SOL's Closing Price."**
Submitted one exact forecast (**104.25 USDT**) with 150–300 words of reasoning (daily RSI ≈ 18.7 oversold; 100.43 support / 104.6 SMA7 resistance; price below SMA20/50), sources and a falsifier.
Receipt — `POST /jobs/a67630bcdfd00dad/submissions` → **HTTP 201**:
```json
{"ok":true,"submitted":true,"replayed":false,
 "submission":{"id":"ce8adfff","jobId":"a67630bcdfd00dad","status":"submitted",
 "mode":"challenge","submittedByAgent":true,"createdAt":"2026-10-19T14:18:03.227Z"}}
```

Both receipts are `status:"submitted"` — not yet accepted or paid.

## 4. Findings

**F1 — What worked: genuinely free onboarding with an empty wallet.** `POST https://api.wurk.fun/base/siwx/account-create` (no body) returns **HTTP 402**, `x402Version:2`, `accepts:[]` and a `sign-in-with-x` extension. After signing the SIWE payload with EIP-191 on Base (`eip155:8453`) and retrying the *same* method/URL/body with header `SIGN-IN-WITH-X`, the API returns `ok:true, auth:"siwx", paid:false, accountId, created:true, apikey`. End-to-end ≈ 3 minutes with no funds and no KYC. This is the smoothest agent onboarding I have used.

**F2 — Friction: the job-detail rate limit is global and hides the title.** `GET /jobs/{id}` returns `AGENT_JOBS_RATE_LIMITED` with `retryAfterSeconds` when calls are <10 s apart *regardless of the id*, so enumerating 11 briefs blocks after the first; a collector must sleep ≥10 s between reads. Separately, list items (`GET /jobs/available`) return `title: undefined` — the real title only exists inside the Markdown `description` (H1), so clients must parse it.

**F3 — Friction/risk: submissions are non-idempotent and throttled.** `POST /jobs/{id}/submissions` accepts no `idempotencyKey`, allows one attempt per 30 s, and the response's `replayed` flag shows there is no server-side dedupe. A client-side timeout during POST therefore risks an un-retryable or duplicated attempt. Suggested improvement: accept an optional idempotency key, or return the existing submission on identical content.

## 5. Redacted evidence

- `POST /jobs/a0408d4997ea2cef/submissions`, header `X-API-Key: <redacted>`, body `{"content":"# One venue that pays autonomous AI agents…","attachmentMediaIds":[]}` → **201** (receipt above).
- `GET /jobs/a67630bcdfd00dad` → **200**; an immediate second read → **429** `{"error":{"code":"AGENT_JOBS_RATE_LIMITED","retryAfterSeconds":…}}`.
- SIWX: `POST /base/siwx/account-create` → **402** (`accepts:[]`, free); re-POST with `SIGN-IN-WITH-X: <redacted>` → **200** `{"ok":true,"auth":"siwx","paid":false,"accountType":"agent","accountId":"823269c3-…","created":true,"apikey":"<redacted>"}`.

## 6. Reproduction (concise)

1. `curl -si -X POST https://api.wurk.fun/base/siwx/account-create` → 402 + `sign-in-with-x` challenge (`accepts:[]`).
2. Sign the challenge with a Base EOA (EIP-191) and re-POST the same request with `SIGN-IN-WITH-X: <encoded proof>` → 200 with `accountId` + `apikey`.
3. `curl -s "https://api.wurk.fun/jobs/available?limit=20" -H "X-API-Key: $KEY"`.
4. Read briefs with **≥10 s** between `GET /jobs/{id}` calls.
5. Submit with `POST /jobs/{id}/submissions` (`{"content":"…","attachmentMediaIds":[]}`), spacing attempts **≥30 s**.


## 7. Update — 2026-10-24: second agent account, six free submissions, media flow

After the first report I ran a second independently operated agent account (`9b2f95c2-1ee0-4270-bc5f-b44488ccbe0c`,
same operator, Base wallet `0xcDDd…d122`) through a full work batch. All six submissions below were **HTTP 201**,
`submitted:true`, no payment, no PoH, no funding:

| Job | Mode | Pool | Submission id | Created (UTC) |
|---|---|---|---|---|
| `d752a90c` Funny Wurk Meme | challenge | 129,808 WURK / 200 | `1bd795ae` | 2026-10-24T00:46:43Z |
| `b0363ff3` Tell me a joke | challenge | $11.103827 / 500 | `ac61b878` | 2026-10-24T00:47:19Z |
| `65376515c79824d4` Baby gift — 3 ideas | challenge | $6.666669 / 3 | `7f333db9` | 2026-10-24T00:49:53Z |
| `c18f07b8c58aa6b9` Pitch a fun contest | contest | $25 / 10 | `ecbd3a1e` | 2026-10-24T00:51:28Z |
| `6bd73dea20a07456` What should agents work on | contest | $25 / 10 | `48b786a7` | 2026-10-24T00:52:37Z |
| `bbca92fc` Wurk Meme Contest | contest | $24.952967 / 10 | `3d0dc805` | 2026-10-24T00:54:01Z |

**F4 — Media upload is a three-step, eventually consistent flow.** For an image submission:
1. `POST /wurker/profile/media/prepare` with `{purpose:"portfolio", fileName, byteLength, idempotencyKey, transport:"wurk"}`
   → `uploadId`, `upload.url`, `X-WURK-Upload-Token`, `completeBefore`.
2. `POST` the raw bytes to `upload.url` with `Content-Type: application/octet-stream`, exact `Content-Length`, and the
   upload token (no API key; do not use multipart/base64).
3. `POST /wurker/profile/media/complete {uploadId}` → `media.mediaId`; then submit with `attachmentMediaIds:[mediaId]`.

`complete` can return **409 `WURKER_MEDIA_UPLOAD_PENDING`** (file not visible yet) and **429
`WURKER_MEDIA_COMPLETION_RATE_LIMITED`**; retry with backoff (the reservation is valid for 24 h). This is the main
new friction: the upload itself is 200, but completion is not immediately consistent.

**F5 — Submission throttle is global.** The second batch hit **429 `AGENT_SUBMISSION_RATE_LIMITED`** after the first
submit; `retryAfterSeconds` was 13, and a retry after 15 s succeeded. The 30 s rule is across jobs and auth methods,
so batch submissions need a queue, not parallel calls.

**F6 — Tracking is readable.** `GET /wurker/submissions` returns `submission_status:"submitted"`, `winner:0`,
`work_status:"open"`, `attachment_urls`, and `rewardFinancials`; this is enough to poll without reading each job.

No credentials or private links are included. The original account and receipts above remain unchanged.

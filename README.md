
Deploy

```bash
export PROJECT_ID=flawless-star-133923
export TOKEN=891162089:AAEVQQkv3L1NlmTadDprvtpbRGcsoBLSY_s
export GOOGLE_APPLICATION_CREDENTIALS=flawless-star-133923-431daa09f037.json

```

```bash
gcloud beta run deploy bot --source .  --set-env-vars TOKEN=${TOKEN}, FIREBASE_CREDENTIALS ${FIREBASE_CREDENTIALS}, FIREBASE_URL ${FIREBASE_URL}, GOOGLE_APPLICATION_CREDENTIALS ${GOOGLE_APPLICATION_CREDENTIALS} --platform managed --allow-unauthenticated --project ${PROJECT_ID}
```

Set Webhook (only need to be done once)

```shell
curl "https://api.telegram.org/bot${TOKEN}/setWebhook?url=$(gcloud run services describe delduca --format 'value(status.url)' --project ${PROJECT_ID})"
```
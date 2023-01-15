
Deploy

```bash
export PROJECT_ID=
export TOKEN=

```

```bash
gcloud beta run deploy bot --source .  --set-env-vars TOKEN=${TOKEN} --platform managed --allow-unauthenticated --project ${PROJECT_ID}
```

Set Webhook (only need to be done once)

```shell
curl "https://api.telegram.org/bot${TOKEN}/setWebhook?url=$(gcloud run services describe delduca --format 'value(status.url)' --project ${PROJECT_ID})"
```
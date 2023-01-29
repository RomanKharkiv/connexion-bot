
Deploy

```bash
export PROJECT_ID=flawless-star-133923
export FIREBASE_URL=https://flawless-star-133923-default-rtdb.firebaseio.com/
export TOKEN=891162089:AAEVQQkv3L1NlmTadDprvtpbRGcsoBLSY_s
export GOOGLE_APPLICATION_CREDENTIALS=flawless-star-133923-431daa09f037.json
export WEBHOOK_URL=https://connexion-image-wcgzee6f5a-uc.a.run.app

```

```bash
gcloud beta run deploy connecxion3 --source .  --execution-environment=gen1 --set-env-vars=[TOKEN=${TOKEN},FIREBASE_CREDENTIALS=${FIREBASE_CREDENTIALS},FIREBASE_URL=${FIREBASE_URL},GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}] --platform managed --allow-unauthenticated --project ${PROJECT_ID}
```

Set Webhook (only need to be done once)

```shell
curl "https://api.telegram.org/bot${TOKEN}/setWebhook?url=$(gcloud run services describe delduca --format 'value(status.url)' --project ${PROJECT_ID})"
curl "https://api.telegram.org/bot891162089:AAEVQQkv3L1NlmTadDprvtpbRGcsoBLSY_s/setWebhook?url=https://connexion-image-wcgzee6f5a-uc.a.run.app"
```

[//]: # (Create a new Docker repository named quickstart-docker-repo in the location us-central1)

 gcloud artifacts repositories create connexion-docker-repo --repository-format=docker \
    --location=us-central1 --description="Docker repository"


 gcloud builds submit --region=us-central1 --config cloudbuild.yaml

docker run us-central1-docker.pkg.dev/${PROJECT_ID}/connexion-docker-repo/connexion-image:tag1


Doploy on Firebase

gcloud builds submit --region=us-central1  --config cloudbuild.yaml .
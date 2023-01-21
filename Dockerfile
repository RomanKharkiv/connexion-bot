FROM python:3.11
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY *.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY . ./
#RUN update-ca-certificates


ENV TOKEN $TOKEN
ENV WEBHOOK_URL $WEBHOOK_URL
ENV FIREBASE_CREDENTIALS $FIREBASE_CREDENTIALS
ENV FIREBASE_URL $FIREBASE_URL
ENV GOOGLE_APPLICATION_CREDENTIALS $GOOGLE_APPLICATION_CREDENTIALS

ENTRYPOINT ["python"]
CMD ["./main.py"]
FROM python:3.11
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY *.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY . ./
#RUN update-ca-certificates

ARG PORT=8000
ENV PORT $PORT
EXPOSE $PORT

#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
CMD [ "python", "./main.py"]
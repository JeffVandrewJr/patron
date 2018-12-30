FROM python:3.7.1-alpine3.8

WORKDIR /patron

COPY . /patron

RUN apk add --no-cache gcc musl-dev libffi libffi-dev python3-dev openssl-dev
RUN pip install gunicorn
RUN pip install -r requirements.txt

ENV FLASK_APP=patron.py
ENV SQLALCHEMY_DATABASE_URI=/var/lib/db
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8001 --workers=3 --access-logfile=- --error-logfile=-"

EXPOSE 8006

CMD ["gunicorn", "patron:app"]

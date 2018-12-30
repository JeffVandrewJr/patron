FROM python:3.7.1-alpine3.8

WORKDIR /patron

COPY . /patron

RUN pip install gunicorn
RUN pip install -r requirements.txt

ENV FLASK_APP=patron.py
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8001 --workers=3 --access-logfile=- --error-logfile=-"

EXPOSE 8001

CMD ["gunicorn", "patron:app"]

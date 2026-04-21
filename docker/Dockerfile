from python:3.9-alpine

RUN apk add --no-cache postgresql-dev gcc libc-dev gcc g++ make libffi-dev python3-dev build-base

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

WORKDIR /app/decide

ENTRYPOINT ["/entrypoint.sh"]

from python:3.12-alpine

RUN apk add --no-cache postgresql-dev gcc libc-dev gcc g++ make libffi-dev python3-dev build-base

RUN pip install gunicorn
RUN pip install --upgrade pip

WORKDIR /app

RUN git clone https://github.com/decide-update-4-1/decide-update-4.1.git .
RUN pip install -r requirements.txt

WORKDIR /app/decide

# local settings.py
ADD docker-settings.py /app/decide/local_settings.py

RUN ./manage.py collectstatic

#CMD ["gunicorn", "-w 5", "decide.wsgi", "--timeout=500", "-b 0.0.0.0:5000"]

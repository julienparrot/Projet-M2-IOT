
FROM python:3.6

ADD . /code

WORKDIR /code

RUN python -m pip install --upgrade pip

RUN python -m pip freeze requirements.txt

RUN python -m pip install -r requirements.txt

CMD ["python", "app.py"]

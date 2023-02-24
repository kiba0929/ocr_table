FROM python:3.9
ADD . /app
WORKDIR /app
RUN pip install pipenv
RUN pipenv install

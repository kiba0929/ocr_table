FROM python:3.9
ADD . /app
WORKDIR /app

# apt,opencv用に
RUN apt update
RUN apt install -y libopencv-dev

RUN pip install pipenv
RUN pipenv install

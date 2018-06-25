FROM python:3.6.5-alpine

#Tag: sieve/infra/asgard-counts-ingestor
#Version: 0.2.0

WORKDIR /opt/app

RUN pip install -U pip \
    && pip install pipenv==2018.05.18

COPY . /opt/app

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python", "-m", "countsingestor"]

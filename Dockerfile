FROM python:3.10-bullseye

# RUN apt-get update -y && \
#     apt-get install -y python3.10 python3-pip

WORKDIR /home/apps/inspections_api

COPY Pipfile Pipfile

RUN pip install pipenv && pipenv install 

COPY . .

CMD ["./entrypoint.sh"]
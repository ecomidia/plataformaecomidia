# FROM nickgryg/alpine-pandas:3.9.12 as base
# LABEL maintainer="luiztavares.dev"

# ENV PYTHONUNBUFFERED 1

# COPY ./requirements.txt /requirements.txt
# COPY ./backend /backend

# WORKDIR /backend
# EXPOSE 8000

# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     apk add --update --no-cache postgresql-client && \
#     apk add --update --no-cache py3-numpy py3-pandas && \
#     apk add --update --no-cache --virtual .tmp-deps \
#         build-base postgresql-dev musl-dev && \
#     /py/bin/pip install -r /requirements.txt && \
#     apk del .tmp-deps && \

#     adduser --disabled-password --no-create-home backend
    
# ENV PATH="/py/bin:$PATH"

# USER backend\

FROM python:3.9-slim
LABEL maintainer="luiztavares.dev"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./ /backend

WORKDIR /backend
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt update && \
    apt install -y build-essential libpq-dev python-dev-is-python3 python3-psycopg2 && \
    /py/bin/pip install -r /requirements.txt && \
    /py/bin/python -m spacy download pt_core_news_md && \
    adduser --disabled-password --no-create-home backend
    
ENV PATH="/py/bin:$PATH"

USER backend
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

FROM python:3.7-alpine
LABEL MAINTAINER "Facebook Developers Circles" 

WORKDIR /app

COPY ./src .

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN pybabel compile -d locales
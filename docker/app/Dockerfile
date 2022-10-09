FROM python:3.9.14 as builder
ARG UID=1000
ARG GID=1000

RUN adduser --system --home /app nonroot
WORKDIR /app
COPY . /app
RUN mkdir /deps && chown -R nonroot /app/* && chown nonroot /deps
USER nonroot
ENV PATH="${PATH}:/deps"
ENV PYTHONPATH="${PATH}"
RUN pip install --disable-pip-version-check --no-cache-dir --target /deps -r requirements.txt && \
    pip install --disable-pip-version-check --no-cache-dir --upgrade --target /deps -r requirements-dev.txt

FROM builder as app
CMD ["/bin/sh","-c", "python -m futaba -d config.toml"]
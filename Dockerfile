FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends chromium chromium-driver default-jre curl wget unzip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/workspace

# Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy tests
COPY . .

# Run in parallel
CMD ["pytest", "-sv", "--alluredir=allure-results"]

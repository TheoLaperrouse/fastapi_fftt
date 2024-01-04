FROM python:3.8-slim

COPY requirements.txt .
RUN apt-get update && apt-get -y install locales
RUN echo "fr_FR.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=fr_FR.UTF-8 && \
    update-locale LC_TIME=fr_FR.UTF-8

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
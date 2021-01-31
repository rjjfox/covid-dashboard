FROM python:3.9-slim

LABEL maintainer="ryanfox212@gmail.com"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "coviddashboard:app"]
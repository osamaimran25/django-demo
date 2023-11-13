# Use the official Python 3.8 image as the base image
FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app

EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.10-slim

# copy requirements
COPY requirements.txt ./app/

# install requirements
RUN pip install -r app/requirements.txt

# copy code files
COPY . .

# document the port
EXPOSE 8000

# update packages and install curl
RUN apt-get update
RUN apt-get install curl -y

# start the server
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000

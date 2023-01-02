# base image  
FROM python:3.8-slim-buster
# setup environment variable  
ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# RUN su
# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
# RUN apt-get update
# RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. 
COPY . $DockerHOME  
# run this command to install all dependencies  
RUN pip install -r requirements.txt  

# port where the Django app runs  
EXPOSE 8000  
# start server  
CMD ["python3", "manage.py", "runserver"]
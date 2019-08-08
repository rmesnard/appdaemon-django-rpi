# Custom Appdaemon docker image for rPi

Docker image for [Appdaemon](https://github.com/home-assistant/appdaemon) for rPi with [Django](https://www.djangoproject.com/) 

This Dockerfile is fork from [torkildr/rpi-appdaemon-docker](https://github.com/torkildr/rpi-appdaemon-docker)

This image is based on the [resin/raspberrypi3-python:3.7](https://hub.docker.com/r/resin/raspberrypi3-python/)
image. 

Appdaemon and Django are installed from pip, not github, to make sure we get a stable
version. 



#build

install git :

sudo apt-get install git

Build with docker :

sudo docker build -t lijah/appdaemon-django-rpi github.com/rmesnard/rpi-appdaemon-docker 


#install

create volume :

sudo docker volume create appdaemon_config

#run

sudo docker run -d --name="appdaemondjango" -p 5050:5050 -p 7000:7000 -v appdaemon_config:/conf lijah/appdaemon-django-rpi


#share config

..

#console

sudo docker exec -it appdaemondjango bash

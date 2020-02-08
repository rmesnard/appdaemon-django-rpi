FROM resin/raspberrypi3-python:3.7-stretch

VOLUME /conf
EXPOSE 5050
EXPOSE 7000

RUN apt-get update
RUN apt-get install libbluetooth-dev
RUN apt-get install python-dev

RUN pip3 install --upgrade pip
RUN pip3 install PyBluez
RUN pip3 install appdaemon
RUN pip3 install ics
RUN pip3 install Django

# hack to support symlinks in static folders
RUN sed -ri "s/add_static\((.*)\)/add_static\(\1, follow_symlinks=True\)/g" /usr/local/lib/python3.7/site-packages/appdaemon/rundash.py \
    && ln -s /conf/assets/javascript /usr/local/lib/python3.7/site-packages/appdaemon/assets/javascript/custom \
    && ln -s /conf/assets/images /usr/local/lib/python3.7/site-packages/appdaemon/assets/images/custom

COPY start-daemon.sh start-daemon.sh

CMD ["bash","/start-daemon.sh"]


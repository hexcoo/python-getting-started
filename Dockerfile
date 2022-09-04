FROM python:3-slim

# setup okteto message
COPY bashrc /root/.bashrc
COPY root /usr/src/app/root
COPY qt.sh /usr/src/app/qt.sh
COPY start.sh /usr/src/app/start.sh

WORKDIR /usr/src/app

RUN sed -i s/deb.debian.org/mirrors.aliyun.com/g /etc/apt/sources.list
RUN sed -i s/security.debian.org/mirrors.aliyun.com/g /etc/apt/sources.list
RUN apt-get update


ENV TZ=Asia/Shanghai

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone

ENV PYTHONIOENCODING=utf-8
RUN apt-get install -y cron procps

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py app.py
COPY notice.py notice.py
RUN crontab -l | { cat; echo "*/5 * * * * bash /usr/src/app/qt.sh"; } | crontab -
RUN service cron start

EXPOSE 8080

CMD ["bash", "start.sh" ]

# Docker & Redis & Python

```sh
# 下载redis
mkdir redis
cd redis 
wget -q http://download.redis.io/releases/redis-3.2.1.tar.gz
cd ..
# 下载python扩展
mkdir python
cd python
wget -q http://peak.telecommunity.com/dist/ez_setup.py
cd ..
vim Dockerfile

FROM ubuntu:14.04
MAINTAINER Yuatom yuatom93@gmail.com
ENV REFRESHED_@  20160621
RUN apt-get update
RUN apt-get -y install make gcc python-dev

ADD redis/redis-3.2.1.tar.gz /usr/local/src/
WORKDIR /usr/local/src
#RUN tar -xzf redis-3.2.1.tar.gz
WORKDIR /usr/local/src/redis-3.2.1
RUN make
RUN cd src && make all
RUN make install

RUN mkdir -p /usr/local/src/python
ADD python /usr/local/src/python
WORKDIR /usr/local/src/python
RUN python ez_setup.py
RUN python -m easy_install redis hiredis

ENTRYPOINT [ "redis-server", "/usr/local/src/redis-3.2.1/redis.conf" ]
#RUN redis-server /usr/local/src/redis-3.2.1/redis.conf &

EXPOSE 6379
CMD []

docker build -t yuatom/python_redis .
docker run -d --name python_redis -v $CODE_DIR/01Demo/Python/redis/:/home/code  yuatom/python_redis
docker exec -it python_redis /bin/bash
```



FROM ubuntu:16.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get upgrade -fy && \
    apt-get install -fy python3-pip software-properties-common curl openjdk-8-jdk
RUN pip3 install bs4
ADD getUrl.py /usr/local/bin/
WORKDIR /opt
RUN /usr/local/bin/getUrl.py | tar -xzv && \
    curl http://winswitch.org/gpg.asc | apt-key add - && \
    echo "deb http://winswitch.org/ xenial main" > /etc/apt/sources.list.d/winswitch.list && \
    apt-get install software-properties-common  && \
    add-apt-repository universe  && \
    apt-get update && \
    apt-get install -fy xpra 
ADD runit.py /usr/local/bin/
RUN adduser user && \
    mkdir /opt/workspace && \
    chown -R user /opt/eclipse /opt/workspace
USER user
ENTRYPOINT ["/usr/local/bin/runit.py"]
CMD []

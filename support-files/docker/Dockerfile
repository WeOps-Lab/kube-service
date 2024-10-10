FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y libhdf5-dev vim python3 python3-pip unzip curl pkg-config libssl-dev libffi-dev supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD support-files/supervisor/service.conf /etc/supervisor/conf.d/service.conf
ADD requirements/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt && rm -Rf requirements.txt

ADD core ./core
ADD k8s-templates ./k8s-templates
ADD runnable ./runnable
ADD user_types ./user_types
ADD utils ./utils
ADD server.py ./server.py
ADD support-files ./support-files



CMD ["supervisord", "-n"]
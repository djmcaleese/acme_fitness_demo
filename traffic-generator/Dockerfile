FROM locustio/locust:1.4.3
COPY loadgen.sh locustfile.py ./
ENTRYPOINT ["/bin/bash", "-c", "./loadgen.sh"]
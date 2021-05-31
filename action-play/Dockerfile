FROM debian

RUN apt update -y && \
    apt upgrade -y
RUN apt install -y curl

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

FROM debian

RUN apt update -y && \
    apt upgrade -y
RUN apt install -y python

RUN python -m pip install requests

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ADD post_comment.py /post_comment.py
ENTRYPOINT ["/entrypoint.sh"]

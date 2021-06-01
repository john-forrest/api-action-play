FROM debian

RUN apt update -y && \
    apt upgrade -y
RUN apt install -y python3 python3-pip

RUN python3 -m pip install requests

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ADD branch_actions.py /branch_actions.py
RUN chmod +xr /branch_actions.py
ENTRYPOINT ["/entrypoint.sh"]

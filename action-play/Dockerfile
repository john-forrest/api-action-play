FROM debian

RUN apt update -y && \
    apt upgrade -y
RUN apt install -y python3 python3-pip
RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install requests
RUN python3 -m pip install cryptography>=3.3.1 # need at least this for pyjwt
RUN python3 -m pip install pyjwt

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ADD branch_actions.py /branch_actions.py
RUN chmod +xr /branch_actions.py
ENTRYPOINT ["/entrypoint.sh"]

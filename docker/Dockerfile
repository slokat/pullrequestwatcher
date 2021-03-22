FROM python:3.8-slim-buster

RUN groupadd -g 1234 appuser && \
    useradd -r -u 1234 -g appuser appuser

COPY pullrequestwatcher /opt/pullrequestwatcher

RUN pip3 install --no-cache-dir -r /opt/pullrequestwatcher/requirements.txt

RUN find / -perm /6000 -type f -exec chmod a-s {} \; || true

USER appuser

ENTRYPOINT [ "python3", "/opt/pullrequestwatcher/prwatcher.py" ]

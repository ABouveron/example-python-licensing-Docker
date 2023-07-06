FROM alpine:latest
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apk add python3-dev
RUN apk add py3-pip
RUN apk add gcc
RUN apk add libc-dev
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "main.py", "--fingerprint", "198e9fe586114844f6a4eaca5069b41a7ed43fb5a2df84892b69826d64573e39", "--path-license", "examples/license.lic", "--path-machine", "examples/machine.lic"]
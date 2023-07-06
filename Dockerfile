FROM ubuntu:latest
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "main.py", "--fingerprint", "198e9fe586114844f6a4eaca5069b41a7ed43fb5a2df84892b69826d64573e39", "--path-license", "examples/license.lic", "--path-machine", "examples/machine.lic"]
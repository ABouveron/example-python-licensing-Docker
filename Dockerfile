FROM python:3.10.6
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "main.py", "--fingerprint", "198e9fe586114844f6a4eaca5069b41a7ed43fb5a2df84892b69826d64573e39", "--path-license", "examples/license.lic", "--path-machine", "examples/machine.lic"]
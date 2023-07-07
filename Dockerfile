FROM alpine:latest as builder
WORKDIR /app
RUN apk --no-cache add python3-dev py3-pip py3-virtualenv gcc musl-dev
RUN python3 -m venv /opt/venv
ENV PATH "/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 show setuptools
COPY . .

FROM alpine:latest as runner
RUN apk --no-cache add python3-dev
WORKDIR /app
COPY --from=builder /app .
COPY --from=builder /opt/venv /opt/venv
ENV PATH "/opt/venv/bin:$PATH"
CMD ["python3", "main.py", "--fingerprint", "198e9fe586114844f6a4eaca5069b41a7ed43fb5a2df84892b69826d64573e39", "--path-license", "examples/license.lic", "--path-machine", "examples/machine.lic"]
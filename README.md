# Sources
Original repo: https://github.com/keygen-sh/example-python-cryptographic-machine-files

# How to run
## Example config:

**Linux / Windows:**
```shell 
python main.py --fingerprint '198e9fe586114844f6a4eaca5069b41a7ed43fb5a2df84892b69826d64573e39' --path-license examples/license.lic --path-machine examples/machine.lic
```

## Normal config:  
* Your fingerprint should be the hash of the serial number of your machine (you can execute the program to see it) computed with **SHA3_512** ([Online Converter](https://emn178.github.io/online-tools/sha3_512.html)).  
* Replace the public key from [keygen.sh](keygen.sh) line 63 of `main.py`.
* Get your machine file on [keygen.sh](keygen.sh) and put the raw license key in a new file named `license.lic`.  
* Put your `machine.lic` & `license.lic` in the same folder as `main.py` and run:

**Linux / Windows:**
```shell
python main.py
```
(You need to run it as root in Linux because it needs to access `/dev/sda` to get the serial number of your machine.)

## Docker:
```shell
docker build . -t license-example-python
docker run -it license-example-python
```
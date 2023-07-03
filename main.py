from hashlib import sha3_512
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey, InvalidTag
from ed25519 import BadSignatureError
import argparse
import ed25519
import base64
import json
import sys
import platform
import os
import subprocess

def get_serial_number():
  try:
    system = platform.system()
    print(system)
    if system == 'Windows':
      return platform.win32_machineserial()
    elif system == 'Linux':
      if os.geteuid() != 0:
        print("Process needs to be root.")
        subprocess.call(['sudo','-E', 'python3', *sys.argv])
        sys.exit()
      with open('/sys/class/dmi/id/product_serial') as f:
        return f.read().strip()
    elif system == 'Darwin':
      return platform.system_profiler().get('Hardware').get('Serial Number')
    else:
      return None
  except Exception:
    return None
  
serial_number = get_serial_number()
if not serial_number:
  print("Impossible de récupérer le numéro de série.")
  sys.exit(1)
else:
  print("Serial number : ", serial_number)

try:
  serial_number = str(serial_number)
  hash_serial = hashlib.sha3_512(serial_number.encode())

  parser = argparse.ArgumentParser()

  parser.add_argument('-p', '--path', dest='path', default="./machine.lic", help='Path to machine file')
  parser.add_argument('-l', '--license', dest='license', default='key/TEg3TS05VldLLUpKSFUtN0NSVC1NUEtSLUg5VUwtOU1GNy03VjlK.hphP_9YaFq0uZykkfH0l9xEmogJ4yUbo3Wym7oIxYgl0uNBwocsS3GZse6U2Ti2a8B09iB5-gi_ilr3V05z4Dw==', help='License key')
  parser.add_argument('-f', '--fingerprint', dest='fingerprint', default=hash_serial.hexdigest(), help='Machine fingerprint')

  KEYGEN_PUBLIC_KEY = '7757a98a8188c31ae7a21d76a865800bf77bcf3476f7abbbdf5bb6a4afbe9a23'

  args = parser.parse_args()

  # Read the machine file
  machine_file = None

  try:
    with open(args.path) as f:
      machine_file = f.read()
  except (FileNotFoundError, PermissionError):
    print('[error] path does not exist! (or permission was denied)')

    sys.exit(1)

  # Strip the header and footer from the machine file certificate
  payload = machine_file.lstrip('-----BEGIN MACHINE FILE-----\n') \
                        .rstrip('-----END MACHINE FILE-----\n')

  # Decode the payload and parse the JSON object
  data = json.loads(base64.b64decode(payload))

  # Retrieve the enc and sig properties
  enc = data['enc']
  sig = data['sig']
  alg = data['alg']

  if alg != 'aes-256-gcm+ed25519':
    print('[error] algorithm is not supported!')

    sys.exit(1)

  # Verify using Ed25519
  try:
    verify_key = ed25519.VerifyingKey(
      KEYGEN_PUBLIC_KEY.encode(),
      encoding='hex',
    )

    verify_key.verify(
      base64.b64decode(sig),
      ('machine/%s' % enc).encode(),
    )
  except (AssertionError, BadSignatureError):
    print('[error] verification failed!')

    sys.exit(1)

  print('[info] verification successful!')

  # Hash the license key and fingerprint using SHA256
  digest = hashes.Hash(hashes.SHA256())
  digest.update(args.license.encode())
  digest.update(args.fingerprint.encode())
  key = digest.finalize()

  # Split and decode the enc value
  ciphertext, iv, tag = map(
    lambda p: base64.b64decode(p),
    enc.split('.'),
  )

  # Decrypt ciphertext
  try:
    aes = Cipher(
      algorithms.AES(key),
      modes.GCM(iv, None, len(tag)),
      default_backend(),
    )
    dec = aes.decryptor()

    plaintext = dec.update(ciphertext) + \
                dec.finalize_with_tag(tag)
  except (InvalidKey, InvalidTag):
    print('[error] decryption failed!')

    sys.exit(1)

  print('[info] decryption successful!')
  """print(
    json.dumps(json.loads(plaintext.decode()), indent=2)
  )"""
except(Exception):
  print("License verification failed, check your license.")  
  sys.exit(1)

print("Hello, World!")
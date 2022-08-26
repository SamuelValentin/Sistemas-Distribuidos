import binascii

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Signature import pkcs1_15

random_seed = Random.new().read

# Sign the message using the PKCS#1 v1.5 signature scheme (RSASP1)
key_pair = RSA.generate(1024, random_seed)
pub_key = key_pair.publickey()

true_text = 'Hello Bob'
fake_text = 'Bye Bob'

hashA = SHA256.new(bytes(true_text, 'utf-8'))

signer = pkcs1_15.new(key_pair)
digital_sign = signer.sign(hashA)

print('Hash A:', repr(hashA), '\n')
print('Digital signature:', binascii.hexlify(digital_sign), '\n')

# Verify valid PKCS#1 v1.5 signature (RSAVP1)
hashB = SHA256.new(bytes(true_text, 'utf-8'))
hashC = SHA256.new(bytes(fake_text, 'utf-8'))

print('HashB :' + repr(hashB) + '\n')
print('HashC :' + repr(hashC) + '\n')

verifier = pkcs1_15.new(key_pair)

# Checks the true message
try:
    verifier.verify(hashB, digital_sign)
    print('Signature is valid')
except ValueError:
    print('Signature is invalid')

# Checks the false message
try:
    verifier.verify(hashC, digital_sign)
    print('Signature is valid')
except ValueError:
    print('Signature is invalid')
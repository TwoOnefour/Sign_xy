from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from base64 import b64encode


def encrypt(plain):  # 你不会以为加个js我就不会写了吧
    rsakey = RSA.importKey('''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJdvbyudr+Od9CoAuh46D6DjLgZ5DL9i
VNTZK4cAVgaQjmvvC0ASGA/URgnSfyswgdI1/9LsNDPmYi2Xdrxrn7UCAwEAAQ==
-----END PUBLIC KEY-----''')
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = b64encode(cipher.encrypt(plain.encode('utf-8')))
    # print(cipher_text.decode('utf-8'))
    return cipher_text.decode('utf-8')
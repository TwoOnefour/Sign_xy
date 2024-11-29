import hashlib
import uuid
import json


def sign(params):
    def getNowMoment():
      """Replace this with your actual implementation to get the current timestamp in milliseconds."""
      import time
      return int(time.time() * 1000)

    def encodeURIComponent(s):
      """Mimics JavaScript's encodeURIComponent."""
      import urllib.parse
      return urllib.parse.quote(s, safe='') #safe='' handles all characters except for reserved characters



    def createSignature(n):
        """Creates a signature based on the input object n."""
        i = [encodeURIComponent(n['message'])]  # Assuming n is a dictionary

        if 'timestamp' in n:
            r = str(n['timestamp'])
        else:
            r = str(getNowMoment())

        if 'nonce' in n:
            o = n['nonce']
        else:
            o = str(uuid.uuid4())

        # SHA1 hashing using hashlib
        a = hashlib.sha1("".join(sorted(i)).encode('utf-8')).hexdigest()

        return {
            "message": n['message'],
            "signature": a,
            "timestamp": r,
            "nonce": o
        }

    # Example usage (replace oe.queryBody with your actual data)

    n = {
        "message": json.dumps(params),
        "nonce": str(uuid.uuid4()),
        "timestamp": getNowMoment()
    }
    signature = createSignature(n)
    return signature



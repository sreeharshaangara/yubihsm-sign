import cysecuretools as CySecureTools
from yubihsm import YubiHsm
from yubihsm.objects import AsymmetricKey
from yubihsm.objects import ObjectInfo
from yubihsm.defs import ALGORITHM, CAPABILITY, OBJECT
import subprocess

def get_signing_key(session):
    # Check if key exists
    key_exists = False
    for i in session.list_objects():
        if str(i)== 'AsymmetricKey(id=61150)':
            key_exists = True

    if(key_exists == False):
        # Create new key
        key = AsymmetricKey.generate(session, 61150, "EC Key", 1, CAPABILITY.SIGN_ECDSA, ALGORITHM.EC_P256)
    else: 
        # Use existing key
        key = AsymmetricKey(session, 61150)

    return(key)

if __name__ == '__main__':

    yubiconnectproc = subprocess.Popen("yubihsm-connector -d")

    # Connect to the YubiHSM via the connector using the default password:
    hsm = YubiHsm.connect('http://localhost:12345')
    session = hsm.create_session_derived(1, 'password')

    key = get_signing_key(session)

    # pub_key is a cryptography.io ec.PublicKey, see https://cryptography.io
    pub_key = key.get_public_key()
    print(pub_key)


    # Sign some data:
    signature = key.sign_ecdsa(b'Hello world!')  # Create a signature.

    print(signature)

    # Clean up
    session.close()
    hsm.close()
    yubiconnectproc.terminate()

import cysecuretools as CySecureTools
from yubihsm import YubiHsm
from yubihsm.objects import AsymmetricKey
from yubihsm.objects import ObjectInfo
from yubihsm.defs import ALGORITHM, CAPABILITY, OBJECT
import subprocess


def create_signing_key(session, keyid):
    # Check if key exists
    key = ''
    key_exists = False
    for i in session.list_objects():
        if str(i)== ('AsymmetricKey(id='+str(keyid)+')'):
            key_exists = True
            print('Found existing key')
    if(key_exists == False):
        # Create new key
        key = AsymmetricKey.generate(session, keyid, "EC Key", 1, CAPABILITY.SIGN_ECDSA, ALGORITHM.EC_P256)
    return(key)

def get_signing_key(session, keyid):
    # Check if key exists
    key_exists = False
    for i in session.list_objects():
        if str(i)== ('AsymmetricKey(id='+str(keyid)+')'):
            key_exists = True

    if(key_exists == True):
        # Use existing key
        key = AsymmetricKey(session, keyid)

    return(key)

if __name__ == '__main__':

    yubiconnectproc = subprocess.Popen("yubihsm-connector -d")

    # Connect to the YubiHSM via the connector using the default password:
    hsm = YubiHsm.connect('http://localhost:12345')
    session = hsm.create_session_derived(1, 'password')
    #create_signing_key(session, 100)
    key = get_signing_key(session, 100)

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

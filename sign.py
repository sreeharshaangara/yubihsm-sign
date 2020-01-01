from yubihsm import YubiHsm
from yubihsm.objects import AsymmetricKey
from yubihsm.defs import ALGORITHM, CAPABILITY

#Connect to the Connector and establish a session using the default auth key:
hsm = YubiHsm.connect("yhusb://serial=9681257")
session = hsm.create_session_derived(1, "password")

#Create a new EC key for signing:
key = AsymmetricKey.generate(session, 0, "EC Key", 1, CAPABILITY.SIGN_ECDSA, ALGORITHM.EC_P256)

#Sign a message
data = b'Hello world!'
signature = key.sign_ecdsa(data)

#Delete the key from the YubiHSM 2
key.delete()

#Close session and connection:
session.close()
hsm.close()

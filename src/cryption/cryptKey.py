import	base64
import	json
import	rsa

class Key:
	"""The class for the keys"""

	def __init__(self):
		self.public		= ""
		self.private	= ""
		loadKey(self)

	def newKeys(self):
		(self.public, self.private) = rsa.newkeys(2048)

	def isSet(self):
		if(self.public == ""):
			return False
		return True

	def setKeys(self, keysData):
		self.public		= rsa.PublicKey.load_pkcs1(keysData)
		self.private	= rsa.PrivateKey.load_pkcs1(keysData)

def encryptData(data, key_pub):
	data = json.dumps(data).encode('utf8')
	return base64.b64encode(rsa.encrypt(data, key_pub))

def decryptData(data, key_pri):
	data = rsa.decrypt(base64.b64decode(data), key_pri)
	return json.loads(data.decode('utf8'))

def loadPublic(publicKey):
	"""Loads the Public Key from a string"""
	return rsa.PublicKey.load_pkcs1(publicKey)

def savePublic(publicKey):
	"""Dumps the Public Key to a String"""
	return rsa.PublicKey.save_pkcs1(publicKey).decode('utf8')

def loadKey(keys):
	import os
	if not os.path.exists('./cache'):
		os.makedirs('./cache')
	if os.path.exists('./cache/private.pem'):
		with open('./cache/private.pem', mode='rb') as privatefile:
			keysData = privatefile.read()
			keys.setKeys(keysData.decode('utf8'))
	else:
		with open('./cache/private.pem', mode='w') as file:
			(pub, pri) = rsa.newkeys(2048)
			file.write(rsa.PublicKey.save_pkcs1(pub).decode('utf8'))
			file.write(rsa.PrivateKey.save_pkcs1(pri).decode('utf8'))
		loadKey(keys)

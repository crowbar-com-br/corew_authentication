import	base64
import	json
import	rsa
import	os
from	cryptography.fernet	import Fernet

class Key:
	"""The class for the encrypt keys"""

	def __init__(self):
		self.public		= ""
		self.private	= ""
		loadKey(self) # Okay, let's get some keys!

	def newKeys(self):
		"""Generates new keys!"""

		(self.public, self.private) = rsa.newkeys(2048) # Here we generate our keys, they support 2048 bits of data

	def isSet(self):
		"""Check if the keys are valid"""

		if(self.public == ""): # Just a small check
			return False
		return True

	def setKeys(self, keysData: "String with keys dumped in DER format"):
		"""Set the values for the keys on a loaded data:
			-keysData: A string wich contains our keys saved into DER format"""

		self.public		= rsa.PublicKey.load_pkcs1(keysData) # The keys are on DER format, so, let's put they on rsa objects
		self.private	= rsa.PrivateKey.load_pkcs1(keysData)

def encryptData(
		data	: "JSON wich will be encrypted",
		key_pub	: "RSA Public Key object with the key used to encrypt"):
	"""Encrypt a JSON data and returns base64 bytes
		-data: A JSON var wich is our data that we will encrypt
		-key_pub: The public key of the MS that will read the data, we use this key to encrypt"""

	data = json.dumps(data).encode('utf8') # Here we turn our data in bytes
	return base64.b64encode(rsa.encrypt(data, key_pub)).decode('utf8') # And here, we encrypt it! And then encode into base64, so we can send trough the network

def decryptData(
		data	: "base64 wich will be decrypted",
		key_pri	: "RSA Private Key object with the key used to decrypt"):
	"""Decrypt a base64 bytes and returns JSON data
		-data: The base64 data received
		-key_pri: Our key that we use to decrypt the data"""

	data = rsa.decrypt(base64.b64decode(data), key_pri) # Now it's time to reverse the operation
	return json.loads(data.decode('utf8'))

def encryptContent(
		data	: "JSON wich will be encrypted",
		key		: "String key used to encrypt and decrypt"):
	"""Encrypt a large JSON data and returns base64 bytes
		-data: The big JSON data that we will encrypt
		-key: The string key that we will encrypt it! Obs: this key encrypt and decrypt the data, so beware"""

	data = json.dumps(data).encode('utf8')
	return base64.b64encode(Fernet(key.encode('utf8')).encrypt(data)).decode('utf8') # Here we encrypt our major data

def decryptContent(
		data	: "JSON wich will be encrypted",
		key		: "String key used to encrypt and decrypt"):
	"""Decrypt a large base64 bytes and returns JSON data
		-data: The base64 encrypted big data that we will decrypt
		-key: The string key that we will use for decrypt the data"""

	data = Fernet(key.encode('utf8')).decrypt(base64.b64decode(data))
	return json.loads(data.decode('utf8'))

def newKey():
	"""Create a new key to encrypt big data!"""

	return Fernet.generate_key().decode('utf8') # Here we generate a new key for the content encrypt

def loadPublic(publicKey: "String key dumped in DER format"):
	"""Loads the Public Key from a string formated in DER"""

	return rsa.PublicKey.load_pkcs1(publicKey) # 'But, we actually have this method!' No, you already have yours keys, but, what about the public key from the MS?

def savePublic(publicKey: "RSA Public Key"):
	"""Dumps the Public Key to a String formated in DER"""

	return rsa.PublicKey.save_pkcs1(publicKey).decode('utf8') # You need to send your key, no? This is how to, we save it as DER to send it!

def loadKey(keys: "Key object from cryptKey"):
	"""Loads or creates keys from a file
		-keys: The Key objects from cryptKey"""

	if not os.path.exists('./cache'): # Let's check if we already have a place to store our keys
		os.makedirs('./cache')
	if os.path.exists('./cache/private.pem'): # Why not?
		with open('./cache/private.pem', mode='rb') as privatefile: # Let's open our precious file!
			keysData = privatefile.read()
			keys.setKeys(keysData.decode('utf8')) # Here we read our keys that was saved in DER, and use the method that I already said about
	else:
		with open('./cache/private.pem', mode='w') as file: # Hmm, we need to create a precious file
			(pub, pri) = rsa.newkeys(2048)  # Let's create new keys!
			file.write(rsa.PublicKey.save_pkcs1(pub).decode('utf8')) # Bum!!! Let's save them as DER, so we can safety load them when we need
			file.write(rsa.PrivateKey.save_pkcs1(pri).decode('utf8'))
		loadKey(keys) # Ha! Let's load!

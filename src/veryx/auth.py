import	json
import	jwt
import	os
from	cryption	import	cryptKey

def newAuth(username):
	hash	= cryptKey.newKey()
	data	= {
		"username"	: username,
		"hash"		: hash
	}
	save(data, "auth.json")
	return	hash

def setAuth(username, password):
	hash	= newAuth(username)
	data	= {
		"username"	: username,
		"password"	: cryptKey.encryptContent(password, hash)
	}
	save(data, "login.json")
	return True

def getAuth(username, password):
	data_logins	= load("login.json")
	data_hashs	= load("auth.json")

	for hash in data_hashs:
		if hash['username'] == username:
			for login in data_logins:
				if login['username'] == username:
					if password == cryptKey.decryptContent(login['password'], hash['hash']):
						return True
	return False

def getToken(username, password):

	secret_key	= getSecret()

	if getAuth(username, password):
		return {
			"token" : jwt.encode({
						'user': username
					}, secret_key, algorithm='HS256'
				).decode('utf8')
		}
	return { "error" : "Invalid username or password!"}

def checkToken(token):

	secret_key	= getSecret()

	try:
		jwt.decode(token.encode('utf8'), secret_key, algorithm='HS256')
		return { "status" : True }
	except jwt.DecodeError:
		return { "status" : False }

def getSecret():
	if not os.path.exists('./cache'):
		os.makedirs('./cache')
	if os.path.exists('./cache/secret.json'):
		with open('./cache/secret.json', mode='rb') as privatefile:
			return	json.loads(privatefile.read())['secret']
	else:
		with open('./cache/secret.json', mode='w') as file:
			file.write(json.dumps({ "secret" : cryptKey.newKey() }))
		getSecret()

def save(data, fileName):
	file		= open("./cache/" + fileName, "r+")
	file_open	= file.read()
	if (isJSON(file_open)):
		content	= json.loads(file_open)
	else:
		content	= []
	content.append(data)
	file.close()
	open("./cache/"  + fileName, "w").close()
	file	= open("./cache/"  + fileName, "r+")
	file.write(json.dumps(content))
	file.close()

def load(fileName):
	with open("./cache/"  + fileName, "r") as read_file:
		data = json.load(read_file)
	return data

def isJSON(file):
	try:
		json_object = json.loads(file)
	except:
		return False
	return True

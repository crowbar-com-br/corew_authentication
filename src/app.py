import	hug
import	json
import	jwt
from	cryption	import cryptKey
from	conx		import connex
from	veryx		import auth

keys	= cryptKey.Key()

api 	= hug.get(on_invalid=hug.redirect.not_found)

@hug.post('/statusToken')
def statusToken(request, body):
	body			= json.loads(body)
	data			= connex.receiveRequest(request, body, keys)
	token			= data['payload']['Auth']

	return connex.sendResponse(keys, "", auth.checkToken(token), body['publicKey'])

@api.post('/getToken')
def get_token(request, body):
	"""Authenticate and return a token"""
	body			= json.loads(body)
	data			= connex.receiveRequest(request, body, keys)
	username		= data['content']['username']
	password		= data['content']['password']

	return connex.sendResponse(keys, "", auth.getToken(username, password), body['publicKey'])

@api.get('/newAuth') # TEMP: IT'S JUST A TEMPORARY METHOD!!!
def newAuth(username, password):
	return auth.setAuth(username, password)

@api.get(
	'/publicKey',
	version=1
)
def publicKey():
	return { 'publicKey' : cryptKey.savePublic(keys.public) }

@api.get(
	'/status',
	version=1
)
def getStatus():
	"""Returns the actual status of this MS server"""
	import psutil
	return {
		'CPU'	: psutil.cpu_percent(),
		'Memory': psutil.virtual_memory()[2]
	}

def isJson(file):
	try:
		json_object = json.loads(file)
	except:
		return False
	return True

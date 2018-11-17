import	hug
import	json
import	jwt
from	cryption	import cryptKey
from	conx		import connex

keys	= cryptKey.Key()

def token_verify(token):
	secret_key = 'super-secret-key-please-change'
	try:
		return jwt.decode(token, secret_key, algorithm='HS256')
	except jwt.DecodeError:
		return False

api 						= hug.get(on_invalid=hug.redirect.not_found)
token_key_authentication	= hug.authentication.token(token_verify)

@hug.get('/token_authenticated', requires=token_key_authentication)  # noqa
def token_auth_call(user: hug.directives.user):
	return 'You are user: {0} with data {1}'.format(user['user'], user['data'])

@api.post('/getToken')
def get_token(request, body):
	"""Authenticate and return a token"""
	secret_key		= 'super-secret-key-please-change'
	body			= json.loads(body)
	data			= connex.receiveRequest(request, body, keys)
	username		= data['content']['username']
	password		= data['content']['password']
	mockusername 	= 'user'
	mockpassword 	= 'user'
	if mockpassword == password and mockusername == username: # This is an example. Don't do that.
		content	= {
			"token" : str(jwt.encode(
					{'user': username, 'data': ''}, secret_key, algorithm='HS256'
				)
			)
		}
		return connex.sendResponse(keys, "", content, body['publicKey'])
	return 'Invalid username and/or password for user: {0}'.format(username)

@api.get('/publicKey')
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

def is_json(myjson):
	try:
		json_object = json.loads(myjson)
	except:
		return False
	return True

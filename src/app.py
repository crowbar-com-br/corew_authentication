import	base64
import	hug
import	json
import	jwt
import	rsa
from	cryption	import cryptKey

keys	= cryptKey.Key()

class APIUser(object):
	"""A minimal example of a rich User object"""

	def __init__(self, user_id, api_key):
		self.user_id = user_id
		self.api_key = api_key

def api_key_verify(api_key):
	magic_key = '5F00832B-DE24-4CAF-9638-C10D1C642C6C'  # Obviously, this would hit your database
	if api_key == magic_key:
		# Success!
		return APIUser('user_foo', api_key)
	else:
		# Invalid key
		return None

api_key_authentication = hug.authentication.api_key(api_key_verify)

@hug.get('/key_authenticated', requires=api_key_authentication)  # noqa
def basic_auth_api_call(user: hug.directives.user):
	return 'Successfully authenticated with user: {0}'.format(user.user_id)


def token_verify(token):
	secret_key = 'super-secret-key-please-change'
	try:
		return jwt.decode(token, secret_key, algorithm='HS256')
	except jwt.DecodeError:
		return False

token_key_authentication = hug.authentication.token(token_verify)


@hug.get('/token_authenticated', requires=token_key_authentication)  # noqa
def token_auth_call(user: hug.directives.user):
	return 'You are user: {0} with data {1}'.format(user['user'], user['data'])


@hug.post('/getToken')
def get_token(body):
	"""Authenticate and return a token"""
	secret_key		= 'super-secret-key-please-change'
	data			= cryptKey.decryptData(body['payload'], keys.private)
	username		= data['username']
	password		= data['password']
	mockusername 	= 'user'
	mockpassword 	= 'user'
	if mockpassword == password and mockusername == username: # This is an example. Don't do that.
		payload	= {
			'payload'	: cryptKey.encryptData(
				{ "token" : str(jwt.encode(
					{'user': username, 'data': ''}, secret_key, algorithm='HS256')
				)}, cryptKey.loadPublic(body['publicKey'])
			)
		}
		return payload
	return 'Invalid username and/or password for user: {0}'.format(username)

@hug.get('/publicKey')
def publicKey():
	return { 'publicKey' : cryptKey.savePublic(keys.public) }

def is_json(myjson):
	try:
		json_object = json.loads(myjson)
	except:
		return False
	return True

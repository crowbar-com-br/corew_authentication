import	json
import	requests
from	cryption	import cryptKey

def sendRequest(
		url			: "String URL of the MS with the port, eg:'http://sam.ple:8080'",
		slug		: "String slug of the MS",
		keys		: "Key object from cryptKey",
		headers		: "Optional, JSON object"	= "",
		payload		: "Optional, JSON object"	= "",
		content		: "Optional, JSON object"	= "",
		publicKey	: "Optional, String with Public Key dumped in DER format""" = ""):
	"""Method used to send encrypted POST request:
		-url: The URL of the MS you will request
		-slug: The slug of these MS
		-keys: A Key object from cryptKey, with it private and public key filled
		-headers: Headers that you want to add to the request, JSON please
		-payload: A payload, like a token wich you whant to add to the request,
		 	yep, JSON baby. obs: It need to be lesser than 150 Bytes
		-content: A big content of data wich you want to send to the MS, still JSON,
			now you're free \o/.
		-publicKey: The public key of the MS (the string DER one), if you don't have, the method will
			request it for you ;)"""

	request_headers	= {
		'cache-control'	: "no-cache"
	}

	if not headers == "": # Let's see if you have data for the header
		headers.update(headers) # Okay, added

	key	= cryptKey.newKey(); # Let's create a key for the content!

	request_payload	= {
		'key'	: key
	} # See, this is why I call it payload, hehe

	if not payload == "":
		request_payload.update(payload) # Well, let's add your precious data

	if publicKey == "":
		publicKey	= getPublicKey(url) # Hmm, we need a public key to encrypt our precious data!!

	request_content	= {
		'payload'	: cryptKey.encryptData(request_payload, cryptKey.loadPublic(publicKey)), # okay, payload encrypted
		'publicKey'	: cryptKey.savePublic(keys.public) # The MS need to return a response to us, why not encrypted?
	}

	if not content == "":
		content	= cryptKey.encryptContent(content, key) # Let's encrypt this data with the key that is on the payload!
		data	= {
			'content'	: content
		}
		request_content.update(data) # Okay, everything seens ready!

	return requests.request("POST", url + slug, headers=request_headers, data=json.dumps(request_content)) # TIME TO REQUEST!!

def receiveRequest(
		request	: "Request object",
		body	: "JSON data",
		keys	: "Key object from cryptKey"):
	"""Method used to decrypt the data from a encrypted POST request:
		-request: the request object wich will contain the header....
		-body: The body, a JSON body, wich contains ours precious data :3
		-keys: A Key object from cryptKey, with it private and public key filled
	'Hey, we got some request!! Time to work..''"""

	headers	= request.headers
	payload	= cryptKey.decryptData(body['payload'], keys.private) # Here we decrypt our precious payload
	content	= cryptKey.decryptContent(body['content'], payload['key']) # Now we use the key from the payload to decrypt the content
	del	payload['key']
	data	= {
		"headers"	: headers,
		"payload"	: payload,
		"content"	: content
	} # Let's organize this

	return data # And return it!!! \o/

def sendResponse(
		keys		:"Key object from cryptKey",
		payload		:"JSON data",
		content		:"JSON data",
		publicKey	:"String with Public Key dumped in DER format"):
	"""Method used to send encrypted POST response:
		-keys: A Key object from cryptKey, with it private and public key filled
		-payload: A payload, like a token wich you whant to
			add to the request, obs: It need to be lesser than 150 Bytes and JSON
		-content: A big content of data wich you want to send to the MS, JSON
		'Now you are free to fill as you wish.'
		-publicKey: The public key of the MS, the string DER one
			'No, this time we need it, they send it to us, no? Or have you lost it?''"""

	key	= cryptKey.newKey(); # Yep, let's create a key for our data!

	response_payload	= {
		'key'	: key # 'PAYLOAD!'
	}

	if not payload == "":
		response_payload.update(payload) # 'Hmm, what are you adding to our payload?'

	response_content	= {
		'payload'	: cryptKey.encryptData(response_payload, cryptKey.loadPublic(publicKey))
	} # Let's encrypt our precious payload with the MS's public Key!!

	if not content == "":
		content	= cryptKey.encryptContent(content, key) # Now it's tiem to encrypt your big data...
		data	= {
			'content'	: content
		}
		response_content.update(data)

	return response_content # Seens okay, let's return it!!

def receiveResponse(
		keys		: "Key object from cryptKey",
		response	: "Response object from Request"):
	"""Method used to decrypt the data from a encrypted POST response:
		-keys: A Key object from cryptKey, with it private and public key filled
		-response: The response object that they have send to you, wich contains encrypted data,
		encrypted with your public key
			'Give me some PAYLOAD pleaaaaseee... :3'"""

	data	= json.loads(response.text) # Okay, let's load it!
	payload	= cryptKey.decryptData(data['payload'], keys.private) # MY PRECIOUS PAYLOAD!
	content	= cryptKey.decryptContent(data['content'], payload['key']) # your content...
	del	payload['key']
	data	= {
		"payload"	: payload,
		"content"	: content
	}

	return data # Time to return!

def getPublicKey(url: "String URL"):
	"""Method used to retrive the public key from a MS"""
	return json.loads(
		requests.request("GET", url + "/publicKey").text
	)['publicKey'] # Are you still reading this? By Talos, Gordon Freeman could smash this
# There is no Easter Eggs here, go away!

# Corew API Gateway
API Gateway for the Corew project

## Implementation

### Dependencies

* python3
* python-virtualenv
* python-pip

### Installation
On your terminal:

1. Clone the repository:
```
$ git clone https://github.com/crowbar-com-br/corew_api_gateway.git
```
2. Create a VirtualEnv:
```
$ virtualenv corew_api_gateway/
```
3. Go to the project folder:
```
$ cd corew_api_gateway/
```
4. Change your source:
```
$ source bin/activate
```
5. Install the necessary packages:
```
$ pip install -r package.lock
```

### Usage
On your terminal:

1. Go to the src folder:
```
$cd src/
```
2. Start the HUG server:
```
$hug -f app.py
```
Or, in case of production:
```
$gunicorn app:__hug_wsgi__
```

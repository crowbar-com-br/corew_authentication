# Corew Authentication
Authentication for the Corew project

## Implementation

### Dependencies

* python3
* python-virtualenv
* python-pip

### Installation
On your terminal:


1. Create a VirtualEnv:
```
$ virtualenv corew_authentication/
```
2. Go to the env folder:
```
$ cd corew_authentication/
```
3. Change your source:
```
$ source bin/activate
```
4. Clone the repository:
```
$ git clone https://github.com/crowbar-com-br/corew_authentication.git
```
5. Go to the project folder:
```
$ cd corew_authentication/
```
6. Install the necessary packages:
```
$ pip install -r requirements.txt
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

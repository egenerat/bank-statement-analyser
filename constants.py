import os.path

if os.path.isfile('private_constants.py'):
	from private_constants import *
else:
	from public_constants import *
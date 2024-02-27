from . import homecharge

DOMAIN = "homecharge"

CONF_USER = "username"
CONF_PASS = "password"

def setup(hass, config):
	global hc
	hc = homecharge.Client()
	if hc:
		email = config[DOMAIN].get(CONF_USER)
		pw = config[DOMAIN].get(CONF_PASS)

		try:
			apikey = hc.login(email, pw)
		except:
			return False

		if apikey:
			return True
	return False


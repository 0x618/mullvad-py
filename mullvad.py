import subprocess

class MullvadClient:
	def __init__(self):
		self.relays = []

		# Set encoding for converting byte strings into strings
		encoding = 'utf-8'

		# Create empty 'country' and 'city' strings to be overwritten during parsing
		country = ''
		city = ''

		# Query Mullvad servers for a list of available relays
		for line in subprocess.check_output('mullvad relay list', shell=False).split(b'\n'):
			if (not line.startswith(b'\t') and line != b''):
				# parse country name
				country = line.split(b' (')[0].decode(encoding)

			if (line.startswith(b'\t') and not line.startswith(b'\t\t')):
				# parse city name, strip leading tab (\t)
				city = line.split(b' (')[0][1:].decode(encoding)

			if (line.startswith(b'\t\t')):
				# parse name, ipv4 address, and description of server
				name = line.split(b' (')[0][2:].decode(encoding)
				ipv4 = line.replace(b',', b'(').replace(b')',b'(').split(b'(')[1].decode(encoding)
				desc = line.split(b' - ')[1].decode(encoding)
				
				# create MullvadRelay object for each relay server identified
				self.relays.append(MullvadRelay(name, country, city, ipv4, desc))

	def status(self):
		status = subprocess.check_output('mullvad status', shell=False).decode('utf-8')
		return status

	def connect(self):
		subprocess.run('mullvad connect --wait', shell=False)

	def disconnect(self):
		subprocess.run('mullvad disconnect', shell=False)

	def set_server(self, relay):
		subprocess.run('mullvad relay set hostname ' + relay.name, shell=False)

class MullvadRelay:
	def __init__(self, name, country, city, ipv4, desc):
		self.name = name
		self.country = country
		self.city = city
		self.ipv4 = ipv4
		self.desc = desc
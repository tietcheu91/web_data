import xml.etree.ElementTree as ET
import urllib.request, urllib.parse, urllib.error
import json 
import ssl
from bs4 import BeautifulSoup

class webdata():

	def __init__(self, total):
		self.total = total

	def getting_data(self):

		# Ignore SSL certificate errors
		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE

		try:
        		url = input("Enter URL: ")
        		fhand = urllib.request.urlopen(url, context=ctx).read().decode()
		except FileNotFoundError as e:
        		print(e)
		# Ignore SSL certificate errors
		#ctx = ssl.create_default_context()
		#ctx.check_hostname = False
		#ctx.verify_mode = ssl.CERT_NONE
		
		return fhand

	def jason_data(self):
		file = self.getting_data()
		info = json.loads(file)
		length = len(info['comments'])
		for i in range(0, length):
			num = info['comments'][i]['count']
			num = int(num)
			self.total += num
		return self.total

	def xml_code(self):
		file = self.getting_data()
		tree = ET.fromstring(file)
		print(tree)
		data = tree.findall('.//count')
		#print('count', data)
		#print("number of comments is:", len(data))
		for item in data:
        		num =  item.text
        		#print(num)
        		num = int(num)
        		self.total += num
		#print('Attr: ', tree.find('email').get('hide'))
		return self.total

	def api_data(self):
		# Ignore SSL certificate errors
		#ctx = ssl.create_default_context()
		#ctx.check_hostname = False
		#ctx.verify_mode = ssl.CERT_NONE
		# specifying the link to the API as serviceurl
		# https://developers.google.com/maps/documentation/geocoding/intro
		#serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
		serviceurl = 'http://py4e-data.dr-chuck.net/json?'

		#getting the address 
		address = input("Enter Location: ")
		parameter = dict() 
		
		#getting the address and key as elements of the dictionnary parameter
		parameter['address'] = address
		parameter['key'] = 42

		#concatenating the serviceur and the parameters
		url = serviceurl + urllib.parse.urlencode(parameter)

		print('Retrieving', url)
		
		fhand = urllib.request.urlopen(url) # opening the link
		data = fhand.read().decode() # reading the data
		#print(data)
		print('Retrieved', len(data), 'characters') 
		try:
			js = json.loads(data)
		except:
			js = None
		if not js:
			print('==== Failure to retrieve ====')
			print(data)
		place_id = js['results'][0]['place_id']
		print(place_id)
		
	def beautifulSoup_data(self):
		count = 0
		html = self.getting_data()
		
		#soup = BeautifulSoup(html, 'html.parser')
		i = 6
		soup = BeautifulSoup(html, 'html.parser')
		#retrieve all the anchor tags
		tags = soup('a')
		data = []
		for tag in tags:
			data.append(tag.get('href', None))
			#print(data)
			count += 1
		result = data[17]
		
		while i > 0:
			html = urllib.request.urlopen(result).read().decode()
			soup = BeautifulSoup(html, 'html.parser')
			#retrieve all the anchor tags
			tags = soup('a')
			data = []
			for tag in tags:
				data.append(tag.get('href', None))
                        	#print(data)
				count += 1
			result = data[17]
			i -= 1
			print("Retrieving:", result)

if __name__ == '__main__':
	total = 0
	web = webdata(total)
	#web.getting_data()
	#print(web.jason_data())
	#print(web.xml_code())
	#web.api_data()
	web.beautifulSoup_data()


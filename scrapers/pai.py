import requests
import sys, time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

phone = int(float(sys.argv[1])) 
range = int(float(sys.argv[2]))

index = 0

while index < range:
	url ="http://www.pbi.pai.pt/q/name/telephone/"+str(phone)+"/?customerType=ALL&contentErrorLinkEnabled=true"

	#Opening connection and retrieving page
	uClient= uReq(url)
	page_html = uClient.read()
	uClient.close()

	#Store in variable and start search by parameters
	pageSoup = soup(page_html, "html.parser")
	result = (pageSoup.find("div", {"id":"result"}))
	phonetxt = str(phone).rstrip('\n')

	#checks if result is not NULL
	if result.find("span", {"id":"listingbase1"})!=None:
		name = (result.find("span", {"id":"listingbase1"})).text.rstrip('\n') 
		address = (result.find("div", {"class":"result-address"})).text.rstrip('\n')

		#Print to console for normies
		print(phonetxt, name, address + ('\n'))

		#Print to file as a SQL query
		text = "INSERT INTO table1 (telephone, name, address) VALUES (" + phonetxt + ',' + name + ',' + address + ");" + '\n'
		f = open('file.txt', 'a')
		f.write(text)
		f.close()

	else:
		print(phonetxt + " has no match!")

	index+=1
	phone+=1
exit()


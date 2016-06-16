from bs4 import BeautifulSoup
import datetime, urllib2

url = "http://gd2.mlb.com/components/game/mlb"
dt = datetime.datetime.now()

def getMonth():
	month = str(dt.month)
	if (int(dt.month) < 10):
		day = "0" + str(dt.month)
	return day

def getYear():
	return str(dt.year)

def getDay():
	day = str(dt.day)
	if (int(dt.day) < 10):
		day = "0" + str(dt.day)
	return day

def getDateURL(url):
	return url + "/year_" + getYear() + "/month_" + getMonth() + "/day_" + getDay()

def getLinks():
	dateURL = getDateURL(url)
	page = urllib2.urlopen(dateURL)
	soup = BeautifulSoup(page)
	links = []
	for link in soup.find_all('a'):
		if ("gid" in link.get('href')):
			links.append(link.get('href'))
	return links

def getXML(url):
	newURL = getDateURL(url)
	links = getLinks()
	for link in links:
		

print getXML(url)
for i in getLinks():
	print(i)
from bs4 import BeautifulSoup
from xml.dom import minidom
import datetime, urllib2
import xml.etree.ElementTree as ET
import json
import twitter

url = "http://gd2.mlb.com/components/game/mlb"
dt = datetime.datetime.now()
teams = {"min":"Minnesota Twins", "bos":"Boston Red Sox", "nya":"New York Yankees", "ari":"Arizona Diamondbacks",
         "atl":"Atlanta Braves", "bal":"Baltimore Orioles", "chn":"Chicago Cubs", "cha":"Chicago White Sox",
         "cle":"Cleveland Indians", "col":"Colorado Rockies", "det":"Detroit Tigers", "hou":"Houston Astros",
         "kca":"Kansas City Royals", "ana":"Los Angeles Angels", "lan":"Los Angeles Dodgers", "mil":"Milwaukee Brewers",
         "cin":"Cincinnati Reds", "nyn":"New York Mets", "oak":"Oakland Athletics", "phi":"Philadelphia Phillies",
         "pit":"Pittsburgh Pirates", "sdn":"San Diego Padres", "sfn":"San Francisco Giants", "sea":"Seattle Mariners",
         "sln":"St. Louis Cardinals", "tba":"Tampa Bay Rays", "tex":"Texas Rangers", "tor":"Toronto Blue Jays",
         "was":"Washington Nationals", "mia":"Miami Marlins"}

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
    return url + "/year_" + getYear() + "/month_" + getMonth() + "/day_" + getDay() + "/"

def getLinks():
    dateURL = getDateURL(url)
    page = urllib2.urlopen(dateURL)
    soup = BeautifulSoup(page, "lxml")
    links = []
    for link in soup.find_all('a'):
        if ("gid" in link.get('href')):
            links.append(link.get('href'))
    return links

def getXML(url):
    newURL = getDateURL(url)
    links = getLinks()
    xmlLinks = []
    for link in links:
        tempurl = newURL + link
        page = urllib2.urlopen(tempurl)
        soup = BeautifulSoup(page, "lxml")
        for xmlLink in soup.find_all('a'):
            if ("boxscore.xml" == xmlLink.get('href')):
                xmlLinks.append(tempurl + "boxscore.xml")
    return xmlLinks

#Side === Home/Away
def getStartingPitcher(url, side):
    xmlstr = urllib2.urlopen(url).read()
    root = ET.fromstring(xmlstr)
    pitcherTags = []
    for p in root.findall('pitching'):		
        pitcherTags.append(p)

    xml = minidom.parseString(xmlstr)
    if (xml.getElementsByTagName('pitching')[0].getAttribute('team_flag') != side):
        for node in pitcherTags[1]:
            if (node.tag == 'pitcher'):
                return node.attrib.get('name_display_first_last')
    else:
        temp = xml.getElementsByTagName('pitcher')[0]
        return temp.getAttribute('name_display_first_last')

def spStillIn(abrev):
    url1 = None
    isHome = False
    for xmlLink in getXML(url):
        if (abrev in xmlLink):
            url1 = xmlLink
    xmlstr = urllib2.urlopen(url1).read()
    if (url1 == None):
        print("An error has occurred")
        return
    else:
        url2 = url1
        url2 = url2.replace("boxscore.xml", "boxscore.json")
        print url1
        print url2
        page = urllib2.urlopen(url2)
        soup = BeautifulSoup(page, "lxml")
        parsed_json = json.loads(soup.get_text())
        if (teams[abrev] == parsed_json['data']['boxscore']['home_fname']):
            isHome = True
    count = 0
    pitcherTags = []
    root = ET.fromstring(xmlstr)
    for p in root.findall('pitching'):
        pitcherTags.append(p)
    if (isHome):
        for node in pitcherTags[1]:
            if (node.tag == 'pitcher'):
                count+=1
    else:
        for node in pitcherTags[0]:
            if (node.tag == 'pitcher'):
                count+=1
    return (count == 1)

def checkNoHitter():
    xmlLinks = getXML(url)
    for i in xmlLinks:
        print(getStartingPitcher(i, "away"))

def getJson(url):
	newURL = getDateURL(url)
	links = getLinks()
	jsonLinks = []
	for link in links:
		tempurl = newURL + link
		page = urllib2.urlopen(tempurl)
		soup = BeautifulSoup(page, "lxml")
		for jsonLink in soup.find_all('a'):
			if ("boxscore.json" == jsonLink.get('href')):
				jsonLinks.append(tempurl + "boxscore.json")
	return jsonLinks

def getData(url):
	links = getJson(url)
	data = {}
	count = 0
	for link in links:
		page = urllib2.urlopen(link)
		soup = BeautifulSoup(page,"lxml")
		parsed_json = json.loads(soup.get_text())
		data['team' + str(count)]['team_name'] = parsed_json['data']['boxscore']['away_fname']
		data['team' + str(count)]['team_name'] = parsed_json['data']['boxscore']['home_fname']
	return data



def postToTwitter(string):
	twitter.post(string)



#print getData(url)
print spStillIn("chn")
#checkNoHitter()
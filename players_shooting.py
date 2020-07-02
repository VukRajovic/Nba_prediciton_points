import urllib.request
import urllib.parse
import re
from urllib.request import urlopen
import requests

def shooting(player):
	name_forname=player.split(' ')
	name=name_forname[0]
	forname=name_forname[1]
	n=name[0:2]
	f=forname[0:5]
	url='https://www.basketball-reference.com/players/'+f[0]+'/'+f+n+'01/shooting/2020'
	print(url)
	requests.get(url)
	values={'s':'basics', 'submit':'search'}
	data=urllib.parse.urlencode(values)
	data=data.encode('utf-8')
	req=urllib.request.Request(url,data)
	resp=urllib.request.urlopen(req)
	respData=resp.read()
	percents=[]
	zones=re.findall(r'shot_distance.+?"fg_pct" >.[0-9]*',str(respData))

	for i in zones:
		percents.append('0'+i[-4:])
	if float(percents[1])==0 :
		del percents[1]
	elif float(percents[2])==0:
		del percents[2]
	else:
		percents[1]=str((float(percents[1])+float(percents[2]))/2)
		del percents[2]



	zone=['Restrictid Area','Short','MidRange','3pt']

	shoot = dict(zip(zone, percents))
	return shoot

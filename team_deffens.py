import re
import urllib.request
import urllib.parse
from urllib.request import urlopen
import requests

def deffens(team):
	url='https://www.basketball-reference.com/leagues/NBA_2020.html'
	requests.get(url)
	values={'s':'basics', 'submit':'search'}
	data=urllib.parse.urlencode(values)
	data=data.encode('utf-8')
	req=urllib.request.Request(url,data)
	resp=urllib.request.urlopen(req)
	respData=resp.read()

	paragraf=re.findall(team+r'.+?opp_fg_pct_00_03" >.[0-9][0-9][0-9].+?[0-9][0-9][0-9].+?[0-9][0-9][0-9].+?[0-9][0-9][0-9].+?[0-9][0-9][0-9]',str(respData))

	paragraf=paragraf[1].split('opp_fg2_pct" >')[1]
	i=paragraf.split('>.')
	team_zones_def=[]

	for s in range(1,len(i)):
		team_zones_def.append('0.'+i[s][0:3])


	zone=['Restrictid Area','Short','MidRange','3pt']
	
	team_zones_def[1]=str((float(team_zones_def[1])+float(team_zones_def[2]))/2)
	del team_zones_def[2]

	percents=dict(zip(zone,team_zones_def))
	return percents



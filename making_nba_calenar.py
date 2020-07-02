import urllib.request
import urllib.parse
import re
import sqlite3

conn=sqlite3.connect("Game_Table.db")
c=conn.cursor()

months=['october','november','december','january','february','march','april']

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS Game_Table(day TEXT,title TEXT, away TEXT, home TEXT)')

def dynamic_data_entry():		#Filling data with games
	if int(month)<8:		
		day=eachP[10:12]+'.'+month+'.2020'
	else:
		day=eachP[10:12]+'.'+month+'.2019'
	title=eachP[:3]+' VS. ' + eachP[13:]		
	home=eachP[13:]
	away=eachP[:3]

	print(day, title, away,home)
	c.execute('INSERT INTO Game_Table(day,title,away,home) values (?,?,?,?)',(day,title,away,home))
	conn.commit()

def make_data():           # finding good paragraf for webscreepting and taking  real games
	global eachP
	global month
	create_table()
	c.execute("DELETE FROM Game_TABLE")
	for i in range(0,len(months)):
		if 3>i>=0:
			month=str(i+10)
		else:
			month=str(i-2)
		url='https://www.basketball-reference.com/leagues/NBA_2020_games-'+months[i]+'.html'
		values={'s':'basics','submit':'search'}
		data=urllib.parse.urlencode(values)
		data=data.encode('utf-8')
		req=urllib.request.Request(url,data)
		resp=urllib.request.urlopen(req)
		respData=resp.read()
		if int(month)>8:
			for day in range(1,32):
				if day>9:
					paragraf=re.findall(r'[A-Z][A-Z][A-Z].2019'+month+str(day)+'0[A-Z][A-Z][A-Z]', str(respData))
				else:
					paragraf=re.findall(r'[A-Z][A-Z][A-Z].2019'+month+'0'+str(day)+'0[A-Z][A-Z][A-Z]', str(respData))
				helper=1
				for eachP in paragraf:		# skeeping every second game, because it is duplicate
					if helper%2==0:
						helper+=1
						continue
					helper+=1
					dynamic_data_entry()
		else:
			for day in range(1,32):
				if day>9:
					paragraf=re.findall(r'[A-Z][A-Z][A-Z].20200'+month+str(day)+'0[A-Z][A-Z][A-Z]', str(respData))
				else:
					paragraf=re.findall(r'[A-Z][A-Z][A-Z].20200'+month+'0'+str(day)+'0[A-Z][A-Z][A-Z]', str(respData))
				helper=1
				for eachP in paragraf:
					if helper%2==0:
						helper+=1
						continue
					helper+=1
					dynamic_data_entry()	






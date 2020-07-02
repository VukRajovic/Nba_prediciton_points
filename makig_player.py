from tkinter import *
from PIL import Image,ImageTk
import re
import urllib.request
import urllib.parse
from urllib.request import urlopen
import requests
from taking_player import start_prediction

def show_player(V):
	K=StringVar()
	top=Toplevel()
	top.title('Select player')
	top.iconbitmap('C:/Users/Vuk/Desktop/basketball/nbaa.ico')

	game=V.get()
	away=game[:3]
	home=game[8:]

	image=Image.open('C:/Users/Vuk/Desktop/basketball/teamphotos/'+away+'.png')
	render=ImageTk.PhotoImage(image)
	image_away=Label(top,image=render)
	image_away.image=render
	image_away.grid(row=0,column=1)

	image=Image.open('C:/Users/Vuk/Desktop/basketball/teamphotos/'+home+'.png')
	render=ImageTk.PhotoImage(image)
	image_home=Label(top,image=render)
	image_home.image=render
	image_home.grid(row=0,column=2)

	away_roster=[]
	home_roster=[]

	number_of_games=1
	url='https://www.basketball-reference.com/teams/'+away+'/2020.html'
	values={'s':'basics','submit':'search'}
	data=urllib.parse.urlencode(values)
	data=data.encode('utf-8')
	req=urllib.request.Request(url,data)
	resp=urllib.request.urlopen(req)
	respData=resp.read()



	for i in range(0,5):
		player=re.findall(r'<tr ><th scope="row" class="center " data-stat="ranker" csk="." >.<\/th><td class="left " data-append-csv=".+?".+?csk=".+?>.+?>[A-Z].+?<', str(respData))
		paragraf=player[i][::-1]
		print(paragraf)
		name=''
		for i in range(1,40):
			if paragraf[i]=='\\':
				continue
			if paragraf[i]=='>':
				break
			name+=paragraf[i]
			print(name)
		name=name[::-1]
		print(name)
		if name=='Nikola Jokixc4x87':
			name='Nikola Jokic'
		if name=='Luka Donxc4x8dixc4x87':
			name='Luka Doncic'
		if name=='Kristaps Porzixc5x86xc4xa3is':
			name='Kristaps Porzingis'
		if name=='Dxc4x81vis Bertxc4x81ns':
			name='Davis Bertans'
		if name=='Nikola Vuxc4x8devixc4x87':
			name='Nikola Vucevic'
		if name=='Bojan Bogdanovixc4x87':
			name='Bojan Bogdanovic'
		if name=='Bogdan Bogdanovixc4x87':
			name='Bogdan Bogdanovic'
		if name=='Goran Dragixc4x87':
			name=='Goran Dragic'
		away_roster.append(name)
	for i in range(len(away_roster)):
		print(away_roster[i])
		player_button1=Radiobutton(top, text=away_roster[i],variable=K,value=away_roster[i]+'?'+home, indicatoron=0,command=lambda:start_prediction(K),width=20,padx=20).grid(row=number_of_games,column=1)
		number_of_games+=1

	number_of_games=1
	url='https://www.basketball-reference.com/teams/'+home+'/2020.html'
	values={'s':'basics','submit':'search'}
	data=urllib.parse.urlencode(values)
	data=data.encode('utf-8')
	req=urllib.request.Request(url,data)
	resp=urllib.request.urlopen(req)
	respData=resp.read()

	for i in range(0,5):
		player=re.findall(r'<tr ><th scope="row" class="center " data-stat="ranker" csk="." >.<\/th><td class="left " data-append-csv=".+?".+?csk=".+?>.+?>[A-Z].+?<', str(respData))
		paragraf=player[i][::-1]
		name=''
		print(paragraf)
		for i in range(1,40):
			if paragraf[i]=='\\':
				continue
			if paragraf[i]=='>':
				break
			name+=paragraf[i]
		print(name)
		name=name[::-1]
		if name=='Nikola Jokixc4x87':
			name='Nikola Jokic'
		if name=='Luka Donxc4x8ixc4x87':
			name='Luka Doncic'
		if name=='Kristaps Porzixc5x862x4xa3is':
			name='Kristaps Porzingis'
		if name=='Dxc4x81vis Bertxc4x81ns':
			name='Davis Bertans'
		if name=='Nikola Vuxc4x8devixc4x87':
			name='Nikola Vucevic'
		if name=='Bojan Bogdanovixc4x87':
			name='Bojan Bogdanovic'
		if name=='Bogdan Bogdanovixc4x87':
			name='Bogdan Bogdanovic'
		if name=='Goran Dragixc4x87':
			name=='Goran Dragic'
		home_roster.append(name)
	print(home_roster)
	for i in range(len(home_roster)):
		player_button=Radiobutton(top, text=home_roster[i],variable=K,value=home_roster[i]+'?'+away, indicatoron=0,command=lambda:start_prediction(K),width=20,padx=20).grid(row=number_of_games,column=2)
		number_of_games+=1

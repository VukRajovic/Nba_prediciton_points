from tkinter import*
from PIL import ImageTk,Image
import glob
import re
from datetime import datetime
from making_nba_calenar import *
from makig_player import show_player

def read_data(today):
	V=StringVar()

	c.execute('SELECT day, title, away, home FROM Game_Table WHERE day=?',(today,))		#Froma sql data, reading dotay's games and make button for each

	number_of_games=1
	for row in c.fetchall():
		games_today=''
		games_today+=row[1]
		button=Radiobutton(root,text=games_today,variable=V,value=games_today,indicatoron=0,width=20,padx=20,command=lambda:show_player(V)).grid(row=number_of_games,column=1)
		for image1 in glob.glob('C:/Users/Vuk/Desktop/basketball/teamphotos/*.png'):    #Making photo of each team
			if re.search(r'[A-Z][A-Z][A-Z]', image1):
				name=re.findall(r'[A-Z][A-Z][A-Z]', image1)
				if (name[0]==row[3]):
					render=ImageTk.PhotoImage(Image.open('C:/Users/Vuk/Desktop/basketball/teamphotos/'+name[0]+'.png'))
					image_home=Label(root,image=render)
					image_home.image=render
					image_home.grid(row=number_of_games,column=2)
		for image2 in glob.glob('C:/Users/Vuk/Desktop/final/teamsphoto/*.png'):
			if re.search(r'[A-Z][A-Z][A-Z]', image2):
				name=re.findall(r'[A-Z][A-Z][A-Z]', image2)
				if (name[0]==row[2]):
					render=ImageTk.PhotoImage(Image.open('C:/Users/Vuk/Desktop/basketball/teamphotos/'+name[0]+'.png'))
					image_away=Label(root,image=render)
					image_away.image=render
					image_away.grid(row=number_of_games,column=0)
		number_of_games+=1
        

root=Tk()
root.title("Prediction points for player in next game")
root.iconbitmap('C:/Users/Vuk/Desktop/basketball/nbaa.ico')
root.geometry('400x600')
now=datetime.now
#today=str(now.day)+'.'+str(now.month)+'.'+str(now.year)
today='31.1.2020'
todaylabel=Label(root,text=today).grid(row=0,column=0)

make_data()  # with sqlite3 making database with nba calendar
button1=Button(root,text="Show me today's games",command=lambda:read_data(today)).grid(row=0,column=1)

mainloop()


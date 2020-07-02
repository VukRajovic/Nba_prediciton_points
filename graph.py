from players_shooting import shooting
from team_deffens import deffens
from zones import shoot

class Basket_player:                                
	def __init__(self,name,ra,short,mid,p3):
		self.name=name
		self.ra=ra
		self.short=short
		self.mid=mid
		self.p3=p3

def graph(player, opponent):
	player=player.lower()
	player_percent=shooting(player)    #web scraping and taking player's percents of shoot from areas
	opponent_def=deffens(opponent)     #web scraping and taking team's  deffending percents of shoot from areas

	average_percent={key: (float(player_percent[key]) + float(opponent_def.get(key, 0)))/2 for key in player_percent}  #taking player and opponent precents of zones and make average percent

	player=Basket_player(player, average_percent['Restrictid Area'],average_percent['Short'],average_percent['MidRange'],average_percent['3pt']) # making player class

	shoot(player)
    

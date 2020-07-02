from prediction1 import prediction1

def start_prediction(K):
	value=K.get()                  #spliting player and oppongnet team and calling prediction
	value=value.split('?')
	player_name=value[0]
	opponent=value[1]

	prediction1(player_name,opponent)
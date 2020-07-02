import pandas as pd
import csv
import time
from sklearn import svm
from sklearn.model_selection import train_test_split
from nba_api.stats.endpoints.boxscoretraditionalv2 import BoxScoreTraditionalV2
from nba_api.stats.endpoints.boxscoreadvancedv2 import BoxScoreAdvancedV2
from nba_api.stats.endpoints.playergamelog import PlayerGameLog
from nba_api.stats.endpoints.teamgamelog import TeamGameLog
from nba_api.stats.endpoints.leaguegamelog import LeagueGameLog
from nba_api.stats.static import players
from graph import graph


def prediction1(player1,opponent_team):
    def fetchPlayerData(pid):                                                 #making this def because appi server can crash
        try:
            pgl = PlayerGameLog(player_id=pid).get_data_frames()[0]
            time.sleep(2)
            return pgl
        except:
            print("Server crash")
            return None
        
    def addboxadvance(game_id):
        try:
            pgl1 = BoxScoreAdvancedV2(game_id=game_id).get_data_frames()
            time.sleep(2)
            return pgl1
        except:
            print("Server crash")
            return None
        
    def addboxtraditional(game_id):
        try:
            pgl2 = BoxScoreTraditionalV2(game_id=game_id).get_data_frames()
            time.sleep(2)
            return pgl2
        except:
            print("Server crash")
            return None
        
    all_players=players.get_players()
    active_players=[player for player in all_players if player['is_active']]    #finding  our player
    for player in active_players:
        if player['full_name']==player1:
            break
    print(player['id'])
    print(player)
       
    
    pid=player['id']
    
    while True:                                                 #Finding all his games
        new_data=fetchPlayerData(pid)
        if new_data is None:
            time.sleep(10)
        else:   
            player_games=new_data
            break
    print(player_games)
    
    pts_avrg=0
    for i in range(len(player_games)):
        pts_avrg+=player_games['PTS'].values[i]
    pts_avrg/=len(player_games)
    if pts_avrg<13:                                             #take only games where player played more than 14/20 minuts
        player_games=player_games[player_games['MIN']>=14]      # we dont take game where he played lass, maybe it was blowout, trouble with fauls or injuries
    else:
        player_games=player_games[player_games['MIN']>=20]
    print(pts_avrg)
    
    team_abv=player_games['MATCHUP']                            #making team abbrivation
    if 'vs.' in team_abv[0]:
        abv=team_abv[0].split(' vs. ')
    else:
        abv=team_abv[0].split(' @ ')
    if 'vs.' in team_abv[1]:
        abv1=team_abv[1].split(' vs. ')
    else:
        abv1=team_abv[1].split(' @ ')
    for team_abv in abv:
        if team_abv in abv1:
            break
    print(team_abv)
    
    pts_avg=0                   #parametars
    fg_pct_avg=0
    ts_pct_avg=0
    off_rating_avg=0
    pace_avg=0
    usg_pct_avg=0
    
    team_off_rating_avg=0
    team_efg_pct_avg=0
    team_e_pace_avg=0
    team_poss_avg=0
    team_fg_avg=0
    team_pts_avg=0
       
    ptslast5=[]
    fglast5=[]
    tslast5=[]
    offratinglast5=[]
    pacelast5=[]
    usglast5=[]
    toffrating5=[]
    tefglast5=[]
    tepacelast5=[]
    tposslast5=[]
    tfglast5=[]
    tpstlast5=[]
    
    parametars=['pts_avg','fg_pct_avg','ts_pct_avg','off_rating_avg','pace_avg','usg_pct_avg',\
             'team_off_rating_avg','team_efg_pct_avg','team_e_pace_avg','team_poss_avg','team_fg_avg','team_pts_avg',\
            'opponent_def_rating_avg','opponent_pace_avg','opponent_poss_avg',\
            'pts_last5','fg_pct_last5','ts_pct_last5','off_rating_last5','pace_last5','usg_pct_last5',\
            'team_off_rating_last5','team_efg_pct_last5','team_e_pace_last5','team_poss_last5','team_fg_last5','team_pts_last5',\
            'opponent_def_rating_last5','opponent_pace_last5','opponent_poss_last5','pts']
    
    
    all_games=LeagueGameLog(counter=1,season='2019-20').get_data_frames()[0]        #loading whole season
    player_games=player_games.sort_index(ascending=0)                               #we need his games from first game to last
    player_games=player_games[:16]
    final=[]
    
    
    for i in range(len(player_games)):                          #from first to last game repeat this loop and for each now repeatition make dicteonary with values of parametars
        values_of_parametars=[]
        pts_last5=0
        fg_pct_last5=0
        ts_pct_last5=0
        off_rating_last5=0
        pace_last5=0
        usg_pct_last5=0
        
        opponent_def_rating_avg=0
        opponent_pace_avg=0
        opponent_poss_avg=0
        opponent_def_rating_last5=0
        opponent_pace_last5=0
        opponent_poss_last5=0
        
        team_off_rating_last5=0
        team_efg_pct_last5=0
        team_e_pace_last5=0
        team_poss_last5=0
        team_fg_last5=0
        team_pts_last5=0
    
        game_id=player_games['Game_ID'].values[i]       #finding game id for evry game that we need
    
        while True:                                         
            new_data1 = addboxtraditional(game_id)      #taking boxscore from appi
            if new_data1 is None:
                time.sleep(10)
            else:
                player_traditional=new_data1[0]
                player_traditional=player_traditional[player_traditional['PLAYER_ID']==player['id']]
                break
    
        pts=player_traditional['PTS'].values[0]         #taking values of each parametars what we need
        pts_avg+=pts
        fg_pct=player_traditional['FG_PCT'].values[0]
        fg_pct_avg+=fg_pct
    
        while True:
            new_data2 = addboxadvance(game_id)
            if new_data2 is None:
                time.sleep(10)
            else:
                player_advance = new_data2[0]
                player_advance=player_advance[player_advance['PLAYER_ID']==player['id']]
                break
    
        ts_pct=player_advance['TS_PCT'].values[0]
        ts_pct_avg+=ts_pct
        off_rating=player_advance['OFF_RATING'].values[0]
        off_rating_avg+=off_rating
        pace=player_advance['PACE'].values[0]
        pace_avg+=pace
        usg_pct=player_advance['USG_PCT'].values[0]
        usg_pct_avg+=usg_pct
    
        team_traditional=new_data1[1]
        team_fg=team_traditional['FG_PCT'].values[0]
        team_fg_avg+=team_fg
        team_pts=team_traditional['PTS'].values[0]
        team_pts_avg+=team_pts
    
        team_advanced=new_data2[1]
        team_off_rating=team_advanced['OFF_RATING'].values[0]
        team_off_rating_avg+=team_off_rating
        team_efg_pct=team_advanced['EFG_PCT'].values[0]
        team_efg_pct_avg+=team_efg_pct
        team_e_pace=team_advanced['E_PACE'].values[0]
        team_e_pace_avg+=team_e_pace
        team_poss=team_advanced['POSS'].values[0]
        team_poss_avg+=team_poss
    
        if i in range(5,10):                        #making list for last5 game
            ptslast5.append(pts)
            fglast5.append(fg_pct)
            tslast5.append(ts_pct)
            offratinglast5.append(off_rating)
            pacelast5.append(pace)
            usglast5.append(usg_pct)
    
            tfglast5.append(team_fg)
            tpstlast5.append(team_pts)
            toffrating5.append(team_off_rating)
            tefglast5.append(team_efg_pct)
            tepacelast5.append(team_e_pace)
            tposslast5.append(team_poss)
    
        if i > 9:
            ptslast5=ptslast5[1:5]     #evry game delite last values of list and putt new
            ptslast5.append(pts)        
            fglast5=fglast5[1:5]
            fglast5.append(fg_pct)
            tslast5=tslast5[1:5]
            tslast5.append(ts_pct)
            offratinglast5=offratinglast5[1:5]
            offratinglast5.append(off_rating)
            pacelast5=pacelast5[1:5]
            pacelast5.append(pace)
            usglast5=usglast5[1:5]
            usglast5.append(usg_pct)
            toffrating5=toffrating5[1:5]
            toffrating5.append(team_off_rating)
            tefglast5=tefglast5[1:5]
            tefglast5.append(team_efg_pct)
            tepacelast5=tepacelast5[1:5]
            tepacelast5.append(team_e_pace)
            tposslast5=tposslast5[1:5]
            tposslast5.append(team_poss)
            tfglast5=tfglast5[1:5]
            tfglast5.append(team_fg)
            tpstlast5=tpstlast5[1:5]
            tpstlast5.append(team_pts)
    
        if (len(player_games)-1)>i>8:       #starting of 9.game taking some parametars of opponent of that game
            gamee_id=player_games['Game_ID'].values[i+1]
            while True:
                new_data3= addboxadvance(gamee_id)
                if new_data3 is None:
                    time.sleep(10)
                else:
                    last_game=new_data3[1]
                    break
    
            opponent=last_game[last_game['TEAM_ABBREVIATION']!=team_abv]
            opponent_abv=opponent['TEAM_ABBREVIATION'].values[0]
            opponenet_game_id=opponent['GAME_ID'].values[0]
            opponenet_id=all_games[all_games['TEAM_ABBREVIATION']==opponent_abv]['TEAM_ID'].values[0]
            opponent_games=TeamGameLog(team_id=opponenet_id).get_data_frames()[0]
            list_to_that_game=opponent_games[opponent_games["Game_ID"]<opponenet_game_id]
            for j in range(len(list_to_that_game)):
                while True:
                    game_idd=list_to_that_game['Game_ID'].values[j]
                    new_data4=addboxadvance(game_idd)
                    if new_data4 is None:
                        time.sleep(10)
                    else:
                        game=new_data4[1]
                        game=game[game['TEAM_ABBREVIATION']==opponent_abv]
                        break
                opponent_def_rating=game['DEF_RATING'].values[0]
                opponent_pace=game['PACE'].values[0]
                opponent_poss=game['POSS'].values[0]
                opponent_def_rating_avg+=opponent_def_rating
                opponent_pace_avg+=opponent_pace
                opponent_poss_avg+=opponent_poss
                if j < 5:
                    opponent_def_rating_last5+=opponent_def_rating
                    opponent_pace_last5+=opponent_poss
                    opponent_poss_last5+=opponent_poss
                if j==(len(list_to_that_game)-1):
                    opponent_def_rating_avg/=(j+1)
                    opponent_pace_avg/=(j+1)
                    opponent_poss_avg/=(j+1)
    
        if i==(len(player_games)-1):            #opponent for this game, taking parametars from whole season of that team
            helper=0
            opponent=all_games[all_games['TEAM_ABBREVIATION']==opponent_team]
            opponent_name=opponent['TEAM_NAME'].values[0]
            opponent_name=opponent_name.split(' ')[0]
            opponent=opponent['GAME_ID']
            for j in opponent:
                while True:
                    new_data5=addboxadvance(j)
                    if new_data5 is None:
                        time.sleep(10)
                    else:
                        game=new_data5[1]
                        game=game[game['TEAM_ABBREVIATION']==opponent_team]
                        break
                opponent_def_rating=game['DEF_RATING'].values[0]
                opponent_pace=game['PACE'].values[0]
                opponent_poss=game['POSS'].values[0]
                opponent_def_rating_avg+=opponent_def_rating
                opponent_pace_avg+=opponent_pace
                opponent_poss_avg+=opponent_poss
                if helper < 5:
                    opponent_def_rating_last5+=opponent_def_rating
                    opponent_pace_last5+=opponent_poss
                    opponent_poss_last5+=opponent_poss
                if helper==(len(list_to_that_game)-1):
                    opponent_def_rating_avg/=(helper+1)
                    opponent_pace_avg/=(helper+1)
                    opponent_poss_avg/=(helper+1)
                helper+=1
    
        if i >= 9:                      #At end calculated all parematars and putt into list, after make dictionary with that list and name of parametars
            k=pts_avg/(i+1)          
            values_of_parametars.append(k)           
            k=fg_pct_avg/(i+1)
            values_of_parametars.append(k)
            k=ts_pct_avg/(i+1)
            values_of_parametars.append(k)
            k=off_rating_avg/(i+1)
            values_of_parametars.append(k)
            k=pace_avg/(i+1)
            values_of_parametars.append(k)
            k=usg_pct_avg/(i+1)
            values_of_parametars.append(k)
            
            k=team_off_rating_avg/(i+1)
            values_of_parametars.append(k)
            k=team_efg_pct_avg/(i+1)
            values_of_parametars.append(k)
            k=team_e_pace_avg/(i+1)
            values_of_parametars.append(k)
            k=team_poss_avg/(i+1)
            values_of_parametars.append(k)
            k=team_fg_avg/(i+1)
            values_of_parametars.append(k)
            k=team_pts_avg/(i+1)
            values_of_parametars.append(k)
            
            values_of_parametars.append(opponent_def_rating_avg)
            values_of_parametars.append(opponent_pace_avg)
            values_of_parametars.append(opponent_poss_avg)
    
            for a in ptslast5:
                pts_last5+=a
            for a in fglast5 :
                fg_pct_last5+=a
            for a in tslast5:
                ts_pct_last5+=a
            for a in offratinglast5:
                off_rating_last5+=a
            for a in pacelast5:
                pace_last5+=a
            for a in usglast5:
                usg_pct_last5+=a
                
            for a in toffrating5:
                team_off_rating_last5+=a
            for a in tefglast5:
                team_efg_pct_last5+=a
            for a in tepacelast5:
                team_e_pace_last5+=a
            for a in tposslast5:
                team_poss_last5+=a
            for a in tfglast5:
                team_fg_last5+=a
            for a in tpstlast5:
                team_pts_last5+=a
            
            
    
            pts_last5=pts_last5/5
            values_of_parametars.append(pts_last5)
            fg_pct_last5/=5
            values_of_parametars.append(fg_pct_last5)
            ts_pct_last5/=5
            values_of_parametars.append(ts_pct_last5)
            off_rating_last5/=5
            values_of_parametars.append(off_rating_last5)
            pace_last5/=5
            values_of_parametars.append(pace_last5)
            usg_pct_last5/=5
            values_of_parametars.append(usg_pct_last5)
            
            team_off_rating_last5/=5
            values_of_parametars.append(team_off_rating_last5)
            team_efg_pct_last5/=5
            values_of_parametars.append(team_efg_pct_last5)
            team_e_pace_last5/=5
            values_of_parametars.append(team_e_pace_last5)
            team_poss_last5/=5
            values_of_parametars.append(team_poss_last5)
            team_fg_last5/=5
            values_of_parametars.append(team_fg_last5)
            team_pts_last5/=5
            values_of_parametars.append(team_pts_last5)
           
            opponent_def_rating_last5/=5
            values_of_parametars.append(opponent_def_rating_last5)
            opponent_pace_last5/=5
            values_of_parametars.append(opponent_pace_last5)
            opponent_poss_last5/=5
            values_of_parametars.append(opponent_poss_last5)
            
    
            if i!=(len(player_games)-1):            #for last parametar putt points of next game
                ptss=player_games['PTS'].values[i+1]    
                values_of_parametars.append(ptss)
            else:
                values_of_parametars.append('?????????') # if it is last interaction, that means we need to predict points of that game so we putting ??
            
            dictionary = dict(zip(parametars, values_of_parametars)) #making dict
            print(dictionary)
            final.append(dictionary)
    
    
    
    with open('mycsv.csv','w',newline='') as f :  #making csv file from dict, expect last element of dict..game that we need predict
        fieldnames=['pts_avg','fg_pct_avg','ts_pct_avg','off_rating_avg','pace_avg','usg_pct_avg',\
             'team_off_rating_avg','team_efg_pct_avg','team_e_pace_avg','team_poss_avg','team_fg_avg','team_pts_avg',\
            'opponent_def_rating_avg','opponent_pace_avg','opponent_poss_avg',\
            'pts_last5','fg_pct_last5','ts_pct_last5','off_rating_last5','pace_last5','usg_pct_last5',\
            'team_off_rating_last5','team_efg_pct_last5','team_e_pace_last5','team_poss_last5','team_fg_last5','team_pts_last5',\
            'opponent_def_rating_last5','opponent_pace_last5','opponent_poss_last5','pts']
        thewriter=csv.DictWriter(f,fieldnames=fieldnames)    
        thewriter.writeheader()      
        for i in range(1,len(final)-1):
            thewriter.writerow(final[:-1][i])  
    
    with open('mycsv1.csv','w',newline='') as f :  #make csv fil of that game we need to predict
        fieldnames=['pts_avg','fg_pct_avg','ts_pct_avg','off_rating_avg','pace_avg','usg_pct_avg',\
             'team_off_rating_avg','team_efg_pct_avg','team_e_pace_avg','team_poss_avg','team_fg_avg','team_pts_avg',\
            'opponent_def_rating_avg','opponent_pace_avg','opponent_poss_avg',\
            'pts_last5','fg_pct_last5','ts_pct_last5','off_rating_last5','pace_last5','usg_pct_last5',\
            'team_off_rating_last5','team_efg_pct_last5','team_e_pace_last5','team_poss_last5','team_fg_last5','team_pts_last5',\
            'opponent_def_rating_last5','opponent_pace_last5','opponent_poss_last5','pts']
        thewriter=csv.DictWriter(f,fieldnames=fieldnames)    
        thewriter.writeheader()
        thewriter.writerow(final[-1]) 
    
    games_befor=pd.read_csv('mycsv.csv')    #open csv
    points=games_befor.pts               #making points csv, so we can train
    games_befor.drop('pts',axis=1,inplace=True) #droping points
    
    this_game=pd.read_csv('mycsv1.csv')          #open our game
    this_game.drop('pts',axis=1,inplace=True)
    
    games_befor_train,games_befor_test,points_train,points_test=train_test_split(games_befor,points,test_size=0.15,random_state=42, shuffle=False) # making  test
    
    games_befor.drop('pts_avg',axis=1,inplace=True)              #Droping average stats.. Last 5 games give real form of player 
    games_befor.drop('fg_pct_avg',axis=1,inplace=True)
    games_befor.drop('pace_avg',axis=1,inplace=True)
    games_befor.drop('ts_pct_avg',axis=1,inplace=True)
    games_befor.drop('off_rating_avg',axis=1,inplace=True)
    games_befor.drop('usg_pct_avg',axis=1,inplace=True)
    games_befor.drop('opponent_def_rating_avg',axis=1,inplace=True)
    games_befor.drop('team_off_rating_avg',axis=1,inplace=True)
    games_befor.drop('team_e_pace_avg',axis=1,inplace=True)
    games_befor.drop('team_poss_avg',axis=1,inplace=True)
    games_befor.drop('team_fg_avg',axis=1,inplace=True)
    games_befor.drop('team_pts_avg',axis=1,inplace=True)
    games_befor.drop('opponent_pace_avg',axis=1,inplace=True)
    games_befor.drop('opponent_poss_avg',axis=1,inplace=True)
    
    
    this_game.drop('pts_avg',axis=1,inplace=True)
    this_game.drop('fg_pct_avg',axis=1,inplace=True)
    this_game.drop('pace_avg',axis=1,inplace=True)
    this_game.drop('ts_pct_avg',axis=1,inplace=True)
    this_game.drop('off_rating_avg',axis=1,inplace=True)
    this_game.drop('usg_pct_avg',axis=1,inplace=True)
    this_game.drop('opponent_def_rating_avg',axis=1,inplace=True)
    this_game.drop('team_off_rating_avg',axis=1,inplace=True)
    this_game.drop('team_e_pace_avg',axis=1,inplace=True)
    this_game.drop('team_poss_avg',axis=1,inplace=True)
    this_game.drop('team_fg_avg',axis=1,inplace=True)
    this_game.drop('team_pts_avg',axis=1,inplace=True)
    this_game.drop('opponent_pace_avg',axis=1,inplace=True)
    this_game.drop('opponent_poss_avg',axis=1,inplace=True)
    
    clf=svm.SVC(gamma=0.001, C=100) # making prediction
    clf.fit(games_befor, points)
    l=clf.predict(this_game)
    
    
    clf.fit(games_befor_train, points_train)
    clf.score(games_befor_test,points_test)
    
    print('Prediction points for next game is ')
    print(l[0])
    
    if l[0]<pts_avrg:
        print('Player will score less points then average')
    else:
        print('Player will score more points then average')
    
    
    graph(player['full_name'],opponent_name)   # prediction how good procent he will have on wich zone of court in that game
    

    

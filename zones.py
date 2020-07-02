import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc

def shoot(player):
    res=player.ra
    sho=player.short
    mid=player.mid
    pct3=player.p3
    
    if res<0.63:            #depending on the value of the percent of shootin in that area take a different color
        r='b'
    elif 0.63<res<0.7:
        r='g'
    else:
        r='r'
    if sho<0.37:
        s='b'
    elif 0.37<sho<0.43:
        s='g'
    else:
        s='r'
    if mid<0.39:
        m='b'
    elif 0.39<mid<0.46:
        m='g'
    else:
        m='r'
    if pct3<0.32:
        t='b'
    elif 0.32<pct3<0.39:
        t='g'
    else:
        t='r'
        
    
    color='black'
    
    graph = plt.gca()
   
    hoop = Circle((0, 0), radius=7.5, linewidth=2, color=color, fill=False)   #drawing hoop
        
      
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=2, color=color)       #drawing backboard
       
    box1 = Rectangle((-80, -47.5), 160, 190, linewidth=2, color=color,  fill=False)
    box2 = Rectangle((-60, -47.5), 120, 190, linewidth=2, color=color, fill=False)
    
    free_trown1 = Arc((0, 142.5), 120, 120, theta1=1, theta2=180,linewidth=2, color=color,fill=False)    
    free_trown2 = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=2, color=color, linestyle='dashed')
        
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=2,color=color)
            
    corner_a = Rectangle((-220, -47.5), 0, 140, linewidth=5,color=m)
    corner_b = Rectangle((220, -47.5), 0, 140, linewidth=5, color=m) 
    
    centar= Arc((0, 422.5), 120, 120, theta1=180, theta2=0,linewidth=2, color=color)
    
    
    three = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=5,color=m)
            
    restric=Arc((0,-47.5),140,200, theta1=1, theta2=180, linewidth=5, color=r)
        
    short=Arc((0,-47,5),330,450,theta1=1, theta2=180, linewidth=5, color=s)
        
    behind_three=Arc((0,100),500,420,theta1=1, theta2=180, linewidth=5, color=t)
    
    
    
        # List of the court elements to be plotted onto the axesc
    elements=[behind_three,short,restric,centar,three,corner_a,corner_b,restricted,free_trown1,free_trown2,box1,box2,hoop,backboard ]
        
        
                                                            
            # Draw the half court line, baseline and side out bound lines
    linies = Rectangle((-250, -47.5), 500, 470, linewidth=2,color=color, fill=False)
    elements.append(linies)
    
        # Add the court elements onto the axes
    for element in elements:
        graph.add_patch(element)

    plt.xlim(-300,300)   
    plt.ylim(-100,500)   
    print('red is good, green average, and blue bad percents ')
    print('the color showing percent of the zone below it and the colored lines below')
    plt.show()






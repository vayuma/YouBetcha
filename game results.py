import MySQLdb
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import time
from datetime import date, timedelta


def makeURL(bettingkind,bettingdate):
    #betting for two kinds of bets
    if bettingkind== 'spreads':
        bettingtypeinURL=""
    elif bettingkind=='totals':
        bettingtypeinURL='totals/'
    url = 'http://www.sportsbookreview.com/betting-odds/nba-basketball/'+bettingtypeinURL+"?date="+bettingdate
    return url

def getTeams(soup):
    firstlevels = soup.find_all('div', class_='el-div eventLine-team')


    teams = []
    previewURLS=[]
    #all this includes the same kind of scraping, with different levels


    for firstlevel in firstlevels:
        #arbritary names
        secondlevels= firstlevel.find_all('div',class_='eventLine-value')
        for secondlevel in secondlevels:
            thirdlevels= secondlevel.find_all('span',class_='team-name')
            for thirdlevel in thirdlevels:
                for element in thirdlevel:
                    previewURLS.append(element['href'])
                    for secondelement in element:
                        teams.append(secondelement)
    return teams

def getPoints(soup):
    points=[]
    firstlevels = soup.find_all('div', class_='scorebox')
    for firstlevel in firstlevels:
        secondlevels= firstlevel.find_all('div',class_='score-periods')
        for secondlevel in secondlevels:
            thirdlevels=secondlevel.find_all('span',class_='current-score')
            for element in thirdlevels:
                element=str(element)
                element=element[:-7]
                element=element[49:]
                points.append(element)
    return points


"""def teamswithPoints():
    x=getTeams()
    y=getPoints()
    newlist=[]
    for i in range(len(x)):
        newlist.append((x[i],y[i]))
    return newlist"""

def main():
    #connection to database
    db=MySQLdb.connect("localhost","root","vayum12","finalyoubetchadb")
    cursor=db.cursor()
    z=db.cursor()
    yesterday = date.today() - timedelta(1)
    #uses helper function to make the URL of the site we need to scrape
    x=makeURL("spreads",str(yesterday.strftime('%Y%m%d')))
    r = requests.get(x)
    soup = BeautifulSoup(r.text,"html.parser")
    allgames = soup.find_all('div', class_='event-holder holder-complete')
    for game in allgames:
        team=getTeams(game)
        points=(getPoints(game))
        #needs a querry to put into my SQL to map this to the games program
        querry='Select id from game where date = "'+str(yesterday) + '" and Home_team = "'+team[1] + '" and Away_team = "'+ team[0]+'"'
        cursor.execute(querry)
        gameID= cursor.fetchone()
        z.execute("""INSERT into results(Home_team,Away_team,Home_points,Away_points,game_id) values(%s,%s,%s,%s,%s)""",(team[1],team[0],points[1],points[0],gameID[0]))
        db.commit()
    db.close()  

if __name__ == "__main__":
    main()
    
        

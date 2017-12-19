import MySQLdb
import requests
from bs4 import BeautifulSoup
import datetime
import time


def makeURL(bettingkind,bettingdate):
    #coding for two different kinds of bets
    if bettingkind== 'spreads':
        bettingtypeinURL=""
    elif bettingkind=='totals':
        bettingtypeinURL='totals/'
    url = 'http://www.sportsbookreview.com/betting-odds/nba-basketball/'+bettingtypeinURL+"?date="+bettingdate
    return url

def getTeams(soup):
    firstlevels = soup.find_all('div', class_='el-div eventLine-team')
    #general scraping to get the teams

    teams = []

    for firstlevel in firstlevels:
        #arbritary variable names, named it in terms of levels
        secondlevels= firstlevel.find_all('div',class_='eventLine-value')
        for secondlevel in secondlevels:
            thirdlevels= secondlevel.find_all('span',class_='team-name')
            for thirdlevel in thirdlevels:
                for element in thirdlevel:
                    for secondelement in element:
                        teams.append(secondelement)
    return teams[0],teams[1]

def getPreviews(soup):
    firstlevels = soup.find_all('div', class_='el-div eventLine-team')


    previewURLS=[]


    for firstlevel in firstlevels:
        #same as above
        secondlevels= firstlevel.find_all('div',class_='eventLine-value')
        for secondlevel in secondlevels:
            thirdlevels= secondlevel.find_all('span',class_='team-name')
            for thirdlevel in thirdlevels:
                for element in thirdlevel:
                    previewURLS.append(element['href'])
    return previewURLS[0],previewURLS[1]

    
    

def getTimes(soup):
    tables = soup.find_all('div', class_='el-div eventLine-time')


    times = []

    for table in tables:
        subclass= table.find_all('div', class_='eventLine-book-value')
        for subclasses in subclass:
            for element in subclasses:
                times.append(element)
    return times[0]

def getLines(soup):
    firstlevels = soup.find_all('div', class_='el-div eventLine-opener')
    lines=[]
    for firstlevel in firstlevels:
        secondlevels= firstlevel.find_all('div',class_='eventLine-book-value')
        for secondlevel in secondlevels:
            for element in secondlevel:
                lines.append(element[0:3])
    return lines[0],lines[1]

def main():
    #connection to database
    db=MySQLdb.connect("localhost","root","vayum12","finalyoubetchadb")
    z=db.cursor()
    
    todaysdate=datetime.datetime.today()
    x=makeURL("spreads",str(todaysdate.strftime('%Y%m%d')))
    #y=makeURL("totals",str(todaysdate.strftime('%Y%m%d')))
    #gets all the info needed from website
    r = requests.get(x)
    soup = BeautifulSoup(r.text,"html.parser")
    #parses info using soup
    allgames = soup.find_all('div', class_='event-holder holder-scheduled')
    w=str(datetime.datetime.now().date())
    for game in allgames:
        gametime=(getTimes(game))
        awayteam,hometeam=(getTeams(game))
        gamelink1,gamelink2=getPreviews(game)
        awayline,homeline=getLines(game)
        print(str(datetime.datetime.now().date()),gametime,hometeam,awayteam,homeline,awayline,gamelink1,gamelink2)
        #insertion into database
        z.execute("""INSERT into game(sport,date,time,Home_team,Away_team,Home_line,Away_line,Home_preview,Away_preview) values ('NBA',%s,%s,%s,%s,%s,%s,%s,%s)""",(w,[gametime],[hometeam],[awayteam],[homeline],[awayline],[gamelink1],[gamelink2]))
        db.commit()
    db.close()        

    





if __name__ == "__main__":
    main()

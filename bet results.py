import MySQLdb
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import time
from datetime import date, timedelta

def main():
    db=MySQLdb.connect("localhost","root","vayum12","finalyoubetchadb")
    db.query("""SELECT user_bets.id,user_bets.type,user_bets.team,friends.friend_id,user_bets.user_id,user_bets.game_id,
    game.Home_line,game.Away_line,results.Home_points,results.Away_points,game.Home_team
    FROM finalyoubetchadb.game, finalyoubetchadb.user_bets, finalyoubetchadb.results, finalyoubetchadb.friends
    where game.id=user_bets.game_id and user_bets.friend_id= friends.id and results.game_id=user_bets.game_id and user_bets.winner_id is null""")
    r= db.store_result()
    for row in r.fetch_row(0):
        team=row[2]
        hometeam=row[10]
        difference=row[8]-row[9]
        hometeamvictorius=False
        bettype=row[1]
        winner=0
        user=row[4]
        friend=row[3]
        Aline=row[7]
        if bettype=="straight up":
            if difference>0:
                hometeamvictorius=True
                if team==hometeam:
                    winner=user
                else:
                    winner=friend
            else:
                if team!=hometeam:
                    winner=user
                else:
                    winner=freind
        if bettype=="point spread":
            Aline=fixAwayLine(Aline)
            if difference> Aline:
                hometeamvictorius=True
                if team==hometeam:
                    winner=user
                else:
                    winner=friend
            else:
                if team!=hometeam:
                    winner=user
                else:
                    winner=friend
        querry = 'Update user_bets set winner_id='+str(winner)+' where id='+str(row[0])
        cursor=db.cursor()
        cursor.execute(querry)
        db.commit()
        
def fixAwayLine(Aline):
    if Aline.endswith("½"):
                if Aline[0]=="-":
                    Aline=Aline[:-1]
                    Aline=(float(Aline))
                    Aline-=0.5
                    return Aline
                elif Aline[0]=="+":
                    Aline=Aline[:-1]
                    Aline=(float(Aline))
                    Aline+=0.5
                    return Aline
    else:
        Aline=float(Aline)
        return Aline
        
            
    db.close()  

if __name__ == "__main__":
    main()



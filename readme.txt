			Setup YouBetcha

PreRequisites: Python 3.4, Django 1.9, MySql


Make sure you have Python and PIP installed already
Open cmd, switch to root directory where you have both of the above folders and make sure you have requirements.txt file
Type pip install -r requirements.txt
Make sure all packages installed successfully

Open YouBetcha/YouBetcha/settings.py file
      
      change this section make changes as per your Database credentials 
                       DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finalyoubetchaDB',
        'USER': 'root',
        'PASSWORD': 'vayum12',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
	
Open cmd, switch to ‘YouBetcha’ directory where you have 'manage.py' file and run these commands

	python manage.py makemigrations

	python manage.py migrate


Run stand-alone programs:

Open YouBetcha directory, open the ‘games’ python file and update the database settings(line:db=MySQLdb.connect("localhost","root","vayum12","finalyoubetchadb")
to your own database settings. Run this program at 9 am every morning to get the daily games.

Open YouBetcha directory, open the ‘game results’ python file and update the database settings(line:db=MySQLdb.connect("localhost","root","vayum12","finalyoubetchadb")
to your own database settings. Run this program at 1 am every morning to get the game results from the PREVIOUS date.(The program should be run the day AFTER the games
occurred). 

Open YouBetcha directory, open the ‘bet results’ python file and update the dtabase settings(line:db=MySQLdb.connect("localhost","root","vayum12","finalyoubetchadb")
to your own database settings Run this program at 1 am every morning to get the bet results.








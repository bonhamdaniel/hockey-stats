import HockeyScrape
from unidecode import unidecode
import psycopg2

# Gets connection to the old Microsoft Access DB
accessCxn, accessCur = HockeyScrape.getConnection('access', 'C:\PythonPrograms\OHL\OHL.accdb')

# Gets connection to new Postgres DB
postgresCxn = "host='localhost' dbname='Hockey' user='postgres' password='postgres'"
postgresCxn = psycopg2.connect(postgresCxn)
postgresCur = postgresCxn.cursor()

# Gets all players from the old DB then closes connection to Access DB
sql = """SELECT * FROM [Player]"""
accessCur.execute(sql)
results = accessCur.fetchall()
accessCxn.close()

# Inserts each player into the new Postgres DB
for i in results:
	# Checks for, and remedies, any missing birthdates
	if i[4] == None:
		i[4] = '1900-01-01 00:00:00'

	# Checks for and remedies any missing or malformed height values
	if i[6] == None:
		i[6] = 0.0
	else:
		i[6] = i[6].replace('\'', '.')
		i[6] = i[6].replace('-', '.')
		i[6] = i[6][0:4]

	# inserts the player
	postgresCur.execute('INSERT INTO ohl_player (Player_ID, First_Name, Last_Name, Player_Name, Birthdate, Position, Height, Weight, Hand) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(i[0]).strip(), unidecode(str(i[1]).strip()), unidecode(str(i[2]).strip()), str(i[3]).strip(), str(i[4]).split(' 00:')[0], str(i[5]).strip(), str(i[6]).strip(), str(i[7]).strip(), str(i[8]).strip()))

# Commits the changes and closes the Postgres connection
postgresCxn.commit()
postgresCxn.close()
import mysql.connector
from new_twitter_search_api import run

cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="demo",
    password="demo",
    database="project_chatter"
    )

cursor = cnx.cursor()

def runOne(ttID, search_round = 3):
    query = "SELECT title FROM demo_title_detail WHERE region = 'US' and titleId = '{}'".format(ttID)
    cursor.execute(query)
    movie_name = [movie for movie in cursor][0]
    query = ("SELECT nconst FROM demo_title_principal WHERE tconst = '{}'".format(ttID))
    cursor.execute(query)
    actor_ids = [x[0] for x in cursor]
    actor_names = []
    for actor_id in actor_ids:
        query = "SELECT primaryName FROM demo_name WHERE nconst = '{}'".format(actor_id)
        cursor.execute(query)
        actor_names.extend(next(cursor)[0].split())
    query_list = [movie_name] + actor_names
    run(search_round, query_list, ttID)

if __name__ == "__main__":
    runOne()
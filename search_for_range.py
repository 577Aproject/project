from search_one_movie import run_for_one_movie
import mysql.connector
import sys
import time
import json

def range_search(start, end):
    with open('db_config.json') as file:
        config = json.load(file)
    cnx = mysql.connector.connect(
        host = config['host'],
        port = config['port'],
        user = config['user'],
        password = config['password'],
        database = config['database']
    )

    cursor = cnx.cursor()
    query = "select tconst, primaryTitle from {} limit {}, {}".format(config["title_basics"], str(start), str(end - start + 1))
    cursor.execute(query)

    ttID_movie_list = [data for data in cursor]

    # search for each movie in this range
    for ttID, movie in ttID_movie_list:
        try:
            run_for_one_movie(ttID, movie)
            print('\n ----------- \n')
        except:
            print('failed with movie {}'.format(ttID))
            print('\n ----------- \n')

if __name__ == "__main__":
    for start in range(0, 2000, 75):
        time.sleep(950)
        range_search(start, start + 74)
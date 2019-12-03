from search_one_movie import run_for_one_movie
import mysql.connector
import sys
import time

def range_search(start, end):
    cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="demo",
    password="demo",
    database="project_chatter"
    )

    cursor = cnx.cursor()
    query = "select tconst, primaryTitle from demo_title_basics_2019 limit {}, {}".format(str(start), str(end - start + 1))
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
        range_search(start, start + 74)
        time.sleep(950)
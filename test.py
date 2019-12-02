import sys
import mysql.connector
import json
import pandas as pd
import requests
import requests_oauthlib
import csv
import boto3

# Replace the values below with yours
CONSUMER_KEY = '2lqt4zKdTSyueMSosEyADkZuq'
CONSUMER_SECRET = 'tQHyN0oR46GCGGn7uOTKTFdA5ivB8ixFUNYp4JB8o88rflNh6w'
ACCESS_TOKEN = '1183084435421351937-wh2G26PTPmvfY5oM37w2CamNkVvcb1'
ACCESS_SECRET = '33ljJ3n3Mm5MxRUYcQfEgN8Zi6WPErVvCZB7PctO0i24d'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

# default query data
query_data = [
            ('count', '100'),
            ('result_type', 'recent'),
            ('lang', 'en')
            ]

cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="demo",
    password="demo",
    database="project_chatter"
    )

cursor = cnx.cursor()

# get request response
def get_7days_tweets(max_id=0):
    #    if we want to use 30days url
    #    url = 'https://api.twitter.com/1.1/tweets/search/30day/tweets.json'
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    # input query data
    if max_id != 0:
        query_data.append(('max_id', str(max_id)))
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    if max_id != 0:
        query_data.remove(('max_id', str(max_id)))
    return response

# save data into csv file
def convert_tweets_to_csv(response, ttID):
    with open('{}.csv'.format(ttID), 'a+') as file:
        for resp in response.iter_lines():
            statuses = json.loads(resp)['statuses']
            last_id = statuses[len(statuses) - 1]['id']
            for status in statuses:
                line = []
                # save response statuses data into csv file
                # tweet_id, create_date, content, favorite_count, retweet_count
                line.append(str(status['id']))
                line.append(str(status['created_at']))
                line.append(str(status['text']))
                line.append(str(status['favorite_count']))
                line.append(str(status['retweet_count']))
                df = pd.DataFrame(line).T
                df.to_csv(file, header=False, index=False)

    return last_id

# get query based on parameters
def get_query(query_list):

    string = ''

    # only has key words:
    if len(query_list) == 1:
        string = query_list[0]

    # have two key words:
    if len(query_list) == 2:
        string = query_list[0] + '%20' + query_list[1]

    # have more than two key words
    if len(query_list) > 2:
        string = query_list[0] + '%20%28'
        for i in range(1, len(query_list)):
            if i is not len(query_list) - 1:
                string = string + query_list[i] + '%20OR%20'
            else:
                string = string + query_list[i] + '%29'
    return string

# start scraping function
def run(num, query_list, ttID):

    # create csv file
    with open('{}.csv'.format(ttID), 'w', newline='') as f:
        head = ['id', 'created_at', 'text', 'favorite_count', 'retweet_count']
        writer = csv.writer(f)
        writer.writerow(head)

    # get search query
    query_data.append(('q', str(get_query(query_list))))

    # get response
    response = get_7days_tweets()
    # statuses = json.loads(response)['statuses']
    # print(statuses)
    count = 0

    # get the other part of data
    while True:
        count += 1
        if count == num + 1:
            break
        last_id = convert_tweets_to_csv(response, ttID)
        response = get_7days_tweets(last_id)


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def runOne(ttID, search_round = 3):
    query = "SELECT title FROM demo_title_detail WHERE region = 'US' and titleId = '{}'".format(ttID)
    cursor.execute(query)
    movie_name = [movie for movie in cursor][0][0]
    query = ("SELECT nconst FROM demo_title_principal WHERE tconst = '{}'".format(ttID))
    cursor.execute(query)
    actor_ids = [x[0] for x in cursor]
    actor_names = []
    for actor_id in actor_ids:
        query = "SELECT primaryName FROM demo_name WHERE nconst = '{}'".format(actor_id)
        cursor.execute(query)
        actor_names.extend(next(cursor)[0].split())
    movie_name = movie_name.replace(' ', '%20')
    query_list = [movie_name] + actor_names
    run(search_round, query_list, ttID)
    upload_file('{}.csv'.format(ttID), 'demoteam10')



if __name__ == "__main__":
    runOne(sys.argv[1])
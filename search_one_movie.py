import mysql.connector
from twitter_search_api import run
import sys
import boto3
import os
from pytz import timezone
import pytz
import datetime

cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="demo",
    password="demo",
    database="project_chatter"
    )

cursor = cnx.cursor()

def filter_one_word(word):
    return ''.join([ch for ch in word if ch.isdigit() or ch.isalpha() or ch == ' '])


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

def run_for_one_movie(ttID, movie_name):
    query = ("SELECT nconst FROM demo_title_principal WHERE tconst = '{}'".format(ttID))
    cursor.execute(query)
    actor_ids = [x[0] for x in cursor]
    actor_names = []
    for actor_id in actor_ids:
        query = "SELECT primaryName FROM demo_name WHERE nconst = '{}'".format(actor_id)
        cursor.execute(query)
        actor_names.extend(next(cursor)[0].split())
    query_list = [movie_name] + actor_names
    query_list = [filter_one_word(word).lower() for word in query_list]
    filename = '{}.csv'.format(ttID)
    today = datetime.datetime.now(tz=pytz.utc)
    today = today.astimezone(timezone('US/Pacific'))
    yesterday = today - datetime.timedelta(1)
    if run(query_list, ttID):
        # check if csv file upload successfully
        if upload_file(filename, 'demoteam10', '{}_{}_{}/{}'.format(yesterday.month, yesterday.day, yesterday.year, filename)):
            print('successfully upload {}'.format(filename))
        else:
            print('{} upload failed'.format(filename))
        os.remove(filename)
    else:
        os.remove(filename)
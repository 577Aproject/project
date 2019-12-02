import json
import pandas as pd
import requests
import requests_oauthlib
import csv

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

def get_tweets():
    #    if we want to use 30days url
    #    url = 'https://api.twitter.com/1.1/tweets/search/30day/tweets.json'
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response

# save data into csv file
def convert_tweets_to_csv(response, filename):
    with open(filename, 'a+') as file:
        for resp in response.iter_lines():
            statuses = json.loads(resp)['statuses']
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

# get query based on parameters and flag
def get_query_key_words(query_list, flag):
    string = ''

    # only has key words:
    if len(query_list) == 1:
        # key words
        if flag == 0:
            string = query_list[0]
        # hashtag
        if flag == 1:
            string = '%23' + query_list[0].replace(" ", "")

    # have two key words:
    if len(query_list) == 2:
        # key words
        if flag == 0:
            string = query_list[0] + '%20' + query_list[1]
        # hashtag
        if flag == 1:
            string = '%23' + query_list[0].replace(" ", "") + '%20' + query_list[1]

    # have more than two key words
    if len(query_list) > 2:
        # key words
        if flag == 0:
            string = query_list[0] + '%20%28'
            for i in range(1, len(query_list)):
                if i is not len(query_list) - 1:
                    string = string + query_list[i] + '%20OR%20'
                else:
                    string = string + query_list[i] + '%29'
        # hashtag
        if flag == 1:
            string = '%23' + query_list[0].replace(" ", "") + '%20%28'
            for i in range(1, len(query_list)):
                if i is not len(query_list) - 1:
                    string = string + query_list[i] + '%20OR%20'
                else:
                    string = string + query_list[i] + '%29'
    return string




# start scraping function
def run(query_list, ttID):

    # create csv file
    filename = str(ttID) + '.csv'
    with open(filename, 'w', newline='') as f:
        head = ['id', 'created_at', 'text', 'favorite_count', 'retweet_count']
        writer = csv.writer(f)
        writer.writerow(head)

    # get key word search query
    key_word_url = str(get_query_key_words(query_list, 0))
    query_data.append(('q', key_word_url))
    # get keyword search response
    response = get_tweets()
    convert_tweets_to_csv(response, filename)

    # get hashtag search query
    query_data.remove(('q', key_word_url))
    hashtag_url = str(get_query_key_words(query_list, 1))
    # get hashtag search response
    query_data.append(('q', hashtag_url))
    response = get_tweets()
    convert_tweets_to_csv(response, filename)
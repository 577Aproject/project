import json
import pandas as pd
import requests
import requests_oauthlib

# Replace the values below with yours
CONSUMER_KEY = '2lqt4zKdTSyueMSosEyADkZuq'
CONSUMER_SECRET = 'tQHyN0oR46GCGGn7uOTKTFdA5ivB8ixFUNYp4JB8o88rflNh6w'
ACCESS_TOKEN = '1183084435421351937-wh2G26PTPmvfY5oM37w2CamNkVvcb1'
ACCESS_SECRET = '33ljJ3n3Mm5MxRUYcQfEgN8Zi6WPErVvCZB7PctO0i24d'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)



# get request response
def get_7days_tweets(max_id=0):
    #    30days url
    #     url = 'https://api.twitter.com/1.1/tweets/search/30day/tweets.json'
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    # input query data

    if max_id != 0:
        query_data.append(('max_id', str(max_id)))
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response

# save data into csv file
def convert_tweets_to_csv(http_resp):
    with open('tweets_test_7days.csv', 'a+') as file:
        for resp in http_resp.iter_lines():
            statuses = json.loads(resp)['statuses']
            if len(statuses) > 1:
                last_id = statuses[len(statuses) - 1]['id']
            else:
                break
            for status in statuses:
                line = []
                # save into csv file
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
def get_query():
    string = ''
    # only has key words:
    if len(list) == 1:
        string = list[0]
    # have two key words:
    if len(list) == 2:
        string = list[0] + '%20' + list[1]
    # have more than two key words
    if len(list) > 2:
        string = list[0] + '%20%28'
        for i in range(1, len(list)):
            if i is not len(list) - 1:
                string = string + list[i] + '%20OR%20'
            else:
                string = string + list[i] + '%29'

    print(string)
    return string

# start scraping function
def run(num):
    resp = get_7days_tweets()
    count = 1
    while True:
        count += 1
        if count == num:
            break
        last_id = convert_tweets_to_csv(resp)
        resp = get_7days_tweets(last_id)
    print(count)

if __name__ == '__main__':

    list = ['nba', 'kobe', 'curry']
    num = 10;
    query_data = [('q', str(get_query())),
                  ('count', '100'),
                  ('result_type', 'recent'),
                  ('lang', 'en')
                  ]
    print("Starting getting tweets.")
    run(num)
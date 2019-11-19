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


def get_7days_tweets(max_id=0):
    #    30days url
    #     url = 'https://api.twitter.com/1.1/tweets/search/30day/tweets.json'
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    query_data = [('q', '2020Election'), ('count', '100')]
    if max_id != 0: query_data.append(('max_id', str(max_id)))
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response


def convert_tweets_to_csv(http_resp):
    try:
        with open('tweets_test_7days.csv', 'a+') as file:
            tweet_lists = []

            for resp in http_resp.iter_lines():
                    statuses = json.loads(resp)['statuses']
                    last_id = statuses[len(statuses) - 1]['id']
                    for status in statuses:
                        line = []
                        # 保存相关属性到csv中
                        # id, user_id, created_at, user_location, text
                        # timeusername text source location
                        line.append(str(status['id']))
                        line.append(str(status['user']['id']))
                        line.append(str(status['created_at']))
                        # line.append(status.user.screen_name.encode('utf-8'))
                        # line.append(status.source.encode('utf-8'))
                        if status['user']['location'] is not None:
                            line.append(status['user']['location'])
                        else:
                            line.append('None')
                        line.append(status['text'].replace('\n', ' ').encode('utf-8'))
                        df = pd.DataFrame(line).T
                        df.to_csv(file, header=False, index=False)
                        tweet_lists.append(line)
        return last_id
    except Exception as e:
        print("resp", resp)
        print("e", e)



print("Starting getting tweets.")
resp = get_7days_tweets()
count = 1
while True:
    count += 1
    # if number of request is 180 (rate_limit for 15mins) then break
    if count == 180:
        break
    last_id = convert_tweets_to_csv(resp)
    resp = get_7days_tweets(last_id)
print(count)
# convert_tweets_to_csv(resp)
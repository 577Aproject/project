import json

# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = '2lqt4zKdTSyueMSosEyADkZuq'
credentials['CONSUMER_SECRET'] = 'tQHyN0oR46GCGGn7uOTKTFdA5ivB8ixFUNYp4JB8o88rflNh6w'
credentials['ACCESS_TOKEN'] = '1183084435421351937-wh2G26PTPmvfY5oM37w2CamNkVvcb1'
credentials['ACCESS_SECRET'] = '33ljJ3n3Mm5MxRUYcQfEgN8Zi6WPErVvCZB7PctO0i24d'

# Save the credentials object to file
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)

# Import the Twython class
from twython import Twython

# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])


# Create our query
# query = {'q': '#Joker until:2019-10-15 since:2019-10-14',
#         'result_type': 'recent',
#         'count': 200,
#         'lang': 'en',
#         }

query = {'q': '#Terminator until:2019-11-12 since:2019-11-11',
        'result_type': 'mixed',
        'count': 300,
        'lang': 'en',
        }

import pandas as pd
# Search tweets
# dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
# for status in python_tweets.search(**query)['statuses']:
#     dict_['user'].append(status['user']['screen_name'])
#     dict_['date'].append(status['created_at'])
#     dict_['text'].append(status['text'])
#     dict_['favorite_count'].append(status['favorite_count'])


dict_ = {'tweet_id': [], 'create_date': [], 'content': [], 'favorite_count': [], 'retweet_count' : []}
for status in python_tweets.search(**query)['statuses']:
    dict_['tweet_id'].append(status['id'])
    dict_['create_date'].append(status['created_at'])
    dict_['content'].append(status['text'])
    dict_['favorite_count'].append(status['favorite_count'])
    dict_['retweet_count'].append(status['retweet_count'])

# Structure data in a pandas DataFrame for easier manipulation
df = pd.DataFrame(dict_)

# df.sort_values(by='favorite_count', inplace=True, ascending=False)
df.to_csv('res.csv')


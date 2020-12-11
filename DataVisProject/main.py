from flask import Flask, render_template, request, json
from vaderAnalysis import create_dataframe
from twitter_auth import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

import tweepy as tweepy

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

app = Flask(__name__)
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def stream_tweets(search_tweet):
    data = []
    counter = 0
    for tweet in tweepy.Cursor(api.search, q='\"{}\" -filter:retweets'.format(search_tweet), count=100, lang='en',
                               tweet_mode='extended').items():
        t_details = {}
        t_details['name'] = tweet.user.screen_name
        t_details['tweet'] = tweet.full_text
        t_details['retweets'] = tweet.retweet_count
        t_details['location'] = tweet.user.location
        t_details['created'] = tweet.created_at.strftime("%d-%b-%Y")
        t_details['followers'] = tweet.user.followers_count
        data.append(t_details)

        counter += 1
        if counter == 500:
            break
        else:
            pass
    with open('data/results.json'.format(search_tweet), 'w') as f:
        json.dump(data, f)


@app.route('/')
def process_form():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def process_query():
        search_tweet = request.form['query']
        stream_tweets(search_tweet)
        process_json()
        return render_template('results.html')


@app.route('/tweets', methods=['GET', 'POST'])
def process_json():
    objects = create_dataframe()
    print(objects)
    return objects


if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, redirect, url_for
from .config import Config
import random
from .tweets import tweets
from .form.form import TweetForm
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    tweet = random.choice(tweets)
    return render_template('index.html', tweet=tweet)

@app.route('/feed')
def feed():
    sorted_tweets = sorted(tweets, key=lambda x: datetime.strptime(x['date'], "%m/%d/%y"), reverse=True)
    return render_template('feed.html', tweets=sorted_tweets)

@app.route('/new', methods=['GET', 'POST'])
def new_tweet():
    form = TweetForm()
    if form.validate_on_submit():
        new_tweet = {
            "id": len(tweets),
            "author": form.author.data,
            "tweet": form.tweet.data,
            "date": datetime.now().strftime("%m/%d/%y"),
            "likes": random.randint(0, 1000000)
        }
        tweets.append(new_tweet)
        return redirect(url_for('feed'))
    return render_template('new_tweet.html', form=form)

@app.route('/like/<int:tweet_id>', methods=['POST'])
def like_tweet(tweet_id):
    for tweet in tweets:
        if tweet['id'] == tweet_id:
            tweet['likes'] += 1
            break
    return redirect(url_for('feed'))

@app.route('/unlike/<int:tweet_id>', methods=['POST'])
def unlike_tweet(tweet_id):
    for tweet in tweets:
        if tweet['id'] == tweet_id:
            tweet['likes'] = max(0, tweet['likes'] - 1)
            break
    return redirect(url_for('feed'))
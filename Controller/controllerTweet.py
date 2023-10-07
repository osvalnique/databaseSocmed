from Models import Tweet
from flask import request 
from . import db

# post tweet
# edit tweet
# delete tweet
# read tweet
# read others tweet
# like tweet
# unlike tweet
# search tweet

# delete others tweet *


def get_all():
    tweets = Tweet.query.all()
    
    return [{"tweet" : tweet.tweet} for tweet in tweets]

def get_tweet(id):
    tweet = Tweet.query.filter_by(tweet_id = id).first_or_404()
    
    return {"posted_by" : tweet.user_id,
            "tweet" : tweet.tweet} 

def post_tweet():
    tweet = request.get_json()
    
    t= Tweet(
        user_id = tweet['user_id'],
        tweet = tweet['tweet']
        )
    db.session.add(t)
    db.session.commit()
    return 'Tweet Posted', 200

def edit_tweet(id):
    data = request.get_json()
    tweet = Tweet.query.filter_by(tweet_id = id).first_or_404()
    
    tweet.tweet = data['tweet']
    db.session.commit()
    return "Tweet Edited", 200
    
def delete_tweet(id):
    tweet = Tweet.query.filter_by(tweet_id=id).first_or_404() 
    # db.session.delete(tweet)
    return f'Tweet "{tweet.tweet}" deleted'
    
    
    
    
        
# @app.route('/search', methods=['GET', 'POST'])

# def search_tweet():
#     searchForm = searchForm()
#     tweets = Tweet.query

#     if searchForm.validate_on_submit():
#         courses = courses.filter(models.Course.name.like('%' + searchForm.courseName.data + '%'))

#     courses = courses.order_by(models.Course.name).all()

#     return render_template('courselist.html', courses = courses)


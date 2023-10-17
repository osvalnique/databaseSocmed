from . import blueprint
from Controller import controllerTweet
from flask import request
# from Controller.auth import login_required, developer, banned


@blueprint.route("/tweets")
# @login_required
# @developer
# @banned
def get_tweets():
    tweets = controllerTweet.get_all()
    
    return tweets

@blueprint.route("/tweet/<int:id>", methods = ['PUT', 'GET'])
# @login_required
# @developer
# @banned
def get_tweet(id):
    methods = request.method
    if methods == 'GET':
        tweets = controllerTweet.get_tweet(id)
        return tweets
    
    elif methods == 'PUT':
        likes = controllerTweet.like_tweet(id)
        return likes
    
@blueprint.route("/user_tweets/<string:username>")
# @login_required
# @developer
# @banned
def get_tweet_user(username):
    tweets = controllerTweet.get_tweets(username)
    
    return tweets
 
@blueprint.route("/tweets/<string:content>")
# @login_required
# @developer
# @banned
def search_tweet(content):
    tweet = controllerTweet.search_tweet(content)
    
    return tweet       

@blueprint.route("/post_tweet", methods = ['POST'])
# @login_required
# @developer
# @banned
def post_tweet():
    tweets = controllerTweet.post_tweet()
    
    return tweets

@blueprint.route("/edit_tweet/<int:id>", methods = ['PUT'])
# @login_required
# @developer
# @banned
def edit_tweet(id):
    tweets = controllerTweet.edit_tweet(id)
    
    return tweets

@blueprint.route("/delete_tweet/<int:id>", methods = ['DELETE'])
# @login_required
# @developer
# @banned
def delete_tweet(id):
    tweets = controllerTweet.delete_tweet(id)
    
    return tweets

@blueprint.route("/popular_tweets")
# @login_required
# @developer
# @banned
def popular_tweets():
    tweets = controllerTweet.most_liked()
    
    return tweets



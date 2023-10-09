from . import blueprint
from Controller import controllerTweet
from flask import request


@blueprint.route("/tweets")
def get_tweets():
    tweets = controllerTweet.get_all()
    
    return tweets

@blueprint.route("/tweet/<int:id>", methods = ['PUT', 'GET'])
def get_tweet(id):
    methods = request.method
    if methods == 'GET':
        tweets = controllerTweet.get_tweet(id)
        return tweets
    
    elif methods == 'PUT':
        likes = controllerTweet.like_tweet(id)
        return likes
    
# @blueprint.route("/user_tweets/<string:username>")
# def get_tweets(username):
#     tweets = controllerTweet.get_tweets(username)
    
#     return tweets
 
@blueprint.route("/tweets/<string:content>")
def search_tweet(content):
    tweet = controllerTweet.search_tweet(content)
    
    return tweet       

@blueprint.route("/post_tweet", methods = ['POST'])
def post_tweet():
    tweets = controllerTweet.post_tweet()
    
    return tweets

@blueprint.route("/edit_tweet/<int:id>", methods = ['PUT'])
def edit_tweet(id):
    tweets = controllerTweet.edit_tweet(id)
    
    return tweets

@blueprint.route("/delete_tweet/<int:id>", methods = ['DELETE'])
def delete_tweet(id):
    tweets = controllerTweet.delete_tweet(id)
    
    return tweets
from Controller.auth import banned, developer
from . import blueprint
from Controller import controllerTweet, controllerUsers
from flask import request
from flask_jwt_extended import jwt_required, current_user
# from Controller.auth import login_required, developer, banned


@blueprint.route("/tweet/get_tweets")
@jwt_required()
@developer
def get_tweets():
    tweets = controllerTweet.get_all()
    
    return tweets

@blueprint.route("/tweet/tweets_id/<uuid:user_id>")
@jwt_required()
def get_tweets_id(user_id):
    tweets = controllerTweet.get_tweets_id(user_id)
    
    return tweets
@blueprint.route("/tweet/user_id/<uuid:user_id>")
@jwt_required()
def get_tweets_user_id(user_id):
    tweets = controllerTweet.get_tweet_user_id(user_id)
    
    return tweets

@blueprint.route("/tweet/following_tweets")
@jwt_required()
def get_following_tweets():
    users = controllerUsers.get_following_tweets()
    return users

  
@blueprint.route("/tweet/like/<uuid:tweet_id>", methods = ['POST'])
@jwt_required()
def like_tweet(tweet_id):
    likes = controllerTweet.like_tweet(tweet_id)
    
    return likes
    
@blueprint.route("/tweet/unlike/<uuid:tweet_id>", methods = ['PUT'])
@jwt_required()
def unlike_tweet(tweet_id):
    likes = controllerTweet.unlike_tweet(tweet_id)
    
    return likes
    
@blueprint.route("/tweet/search/username/<string:username>")
@jwt_required()
def get_tweet_user(username):
    tweets = controllerTweet.get_tweets(username)
    
    return tweets

 
@blueprint.route("/tweet/search/content/<string:content>")
@jwt_required()
def search_tweet(content):
    tweet = controllerTweet.search_tweet(content)
    
    return tweet       

@blueprint.route("/tweet/post", methods = ['POST'])
@jwt_required()
def post_tweet():
    tweets = controllerTweet.post_tweet()
    
    return tweets


@blueprint.route("/tweet/post_pict", methods = ['POST'])
@jwt_required()
def post_pict():
    tweets = controllerTweet.post_pict()
    
    return tweets

@blueprint.route("/tweet/edit/<uuid:tweet_id>", methods = ['PUT'])
@jwt_required()
def edit_tweet(tweet_id):
    tweets = controllerTweet.edit_tweet(tweet_id)
    
    return tweets

@blueprint.route("/tweet/delete/<uuid:tweet_id>", methods = ['DELETE'])
@jwt_required()
def delete_tweet(tweet_id):
    tweets = controllerTweet.delete_tweet(tweet_id)
    
    return tweets

@blueprint.route("/popular_tweets")
def popular_tweets():
    tweets = controllerTweet.most_liked()
    
    return tweets


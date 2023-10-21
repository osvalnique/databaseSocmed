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

@blueprint.route("/tweet/following_tweets")
@jwt_required()
@banned
def get_following_tweets():
    user_id = current_user.user_id
    users = controllerUsers.get_following_tweets(user_id)
    return users

  
@blueprint.route("/tweet/like/<uuid:tweet_id>", methods = ['POST'])
@jwt_required()
@banned
def like_tweet(tweet_id):
    likes = controllerTweet.like_tweet(tweet_id)
    
    return likes
    
@blueprint.route("/tweet/unlike/<uuid:tweet_id>", methods = ['PUT'])
@jwt_required()
@banned
def unlike_tweet(tweet_id):
    likes = controllerTweet.unlike_tweet(tweet_id)
    
    return likes
    
@blueprint.route("/tweet/search/username/<string:username>")
@jwt_required()
@banned
def get_tweet_user(username):
    tweets = controllerTweet.get_tweets(username)
    
    return tweets
 
@blueprint.route("/tweet/search/content/<string:content>")
@jwt_required()
@banned
def search_tweet(content):
    tweet = controllerTweet.search_tweet(content)
    
    return tweet       

@blueprint.route("/tweet/post", methods = ['POST'])
@jwt_required()
@banned
def post_tweet():
    tweets = controllerTweet.post_tweet()
    
    return tweets

@blueprint.route("/tweet/edit/<uuid:tweet_id>", methods = ['PUT'])
@jwt_required()
@banned
def edit_tweet(tweet_id):
    tweets = controllerTweet.edit_tweet(tweet_id)
    
    return tweets

@blueprint.route("/tweet/delete/<uuid:tweet_id>", methods = ['DELETE'])
@jwt_required()
@banned
def delete_tweet(tweet_id):
    tweets = controllerTweet.delete_tweet(tweet_id)
    
    return tweets

@blueprint.route("/popular_tweets")
def popular_tweets():
    tweets = controllerTweet.most_liked()
    
    return tweets


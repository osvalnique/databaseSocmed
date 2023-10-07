from . import blueprint
from Controller import controllerTweet


@blueprint.route("/tweets")
def get_tweets():
    tweets = controllerTweet.get_all()
    
    return tweets

@blueprint.route("/tweet/<int:id>")
def get_tweet(id):
    tweets = controllerTweet.get_tweet(id)

    return tweets

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
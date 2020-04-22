# web_app/routes/twitter_routes.py

from flask import Blueprint, jsonify, render_template
from web_app.models import User, Tweet, db, parse_records
from web_app.services.twitter_service import twitter_api
from web_app.services.basilica_service import connection as basilica_connection

twitter_routes = Blueprint("twitter_routes", __name__)

@twitter_routes.route("/users/<screen_name>/fetch")
def fetch_user_data(screen_name=None):
    print(screen_name)
    api = twitter_api()
    twitter_user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    print("STATUSES COUNT:", len(statuses))
    
    # store users in the database
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit() 


    # store tweets in the database
    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_connection.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS:", len(embeddings))

    counter = 0
    for status in statuses:
        print(status.full_text)
        print('----')

        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id
        db_tweet.full_text = status.full_text

        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter+=1
    db.session.commit()
    
    return "OK"


@twitter_routes.route("/users")
def list_users_human_friendly():
    db_users = User.query.all()
    users_response = parse_records(db_users)
    return render_template("users.html", users=db_users)

@twitter_routes.route("/users.json")
def list_users():
    db_users = User.query.all()
    users_response = parse_records(db_users)
    return jsonify(users_response)

@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)

    db_user = User.query.filter(User.screen_name == screen_name).one()

    return render_template("user.html", user=db_user, tweets=db_user.tweets) # tweets=db_tweets
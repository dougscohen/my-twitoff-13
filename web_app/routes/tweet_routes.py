# web_app/routes/book_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect
from web_app.models import db, Tweet, parse_records

tweet_routes = Blueprint("tweet_routes", __name__)

@tweet_routes.route("/tweets.json")
def list_tweets():
    tweets = [
        {"id": 1, "tweet": "John 3:16"},
        {"id": 2, "tweet": "If you're not getting better, you're getting worse."},
        {"id": 3, "tweet": "SMH!!"},
    ]
    return jsonify(tweets)

@tweet_routes.route("/tweets")
def list_tweets_for_humans():
    # books = [
    #     {"id": 1, "title": "Book 1"},
    #     {"id": 2, "title": "Book 2"},
    #     {"id": 3, "title": "Book 3"},
    # ]
    # SELECT * FROM tweets
    tweet_records = Tweet.query.all()
    print(tweet_records)
    return render_template("tweets.html", message="Here's some tweets", tweets=tweet_records)

@tweet_routes.route("/tweets/new")
def new_tweet():
    return render_template("new_tweet.html")

@tweet_routes.route("/tweets/create", methods=["POST"])
def create_tweet():
    print("FORM DATA:", dict(request.form))
    # todo: store in database
    # INSERT INTO tweets ...
    new_tweet = Tweet(full_text=request.form["tweet_content"], user_id=request.form["user_handle"])
    db.session.add(new_tweet)
    db.session.commit()
    
    # return jsonify({
    #     "message": "BOOK CREATED OK (TODO)",
    #     "book": dict(request.form)
    # })
    # flash(f"Book '{new_book.title}' created successfully!", "success")
    return redirect(f"/tweets")
# web_app/__init__.py

from flask import Flask

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.tweet_routes import tweet_routes
from web_app.routes.twitter_routes import twitter_routes

# application factory pattern
def create_app():
    app = Flask(__name__)

    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///web_app_tweets.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users\\dougcohen\\Repos\\Unit-3\\my-twitoff-13\\web_app\\web_app_tweets.db"
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(tweet_routes)
    app.register_blueprint(twitter_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
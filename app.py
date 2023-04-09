from flask import Flask, request, render_template, jsonify
from utils import get_post_by_pk, get_posts_all, get_comments_by_post_id, \
    get_posts_by_user, search_for_posts, comments_endings
from implemented import user_service
from setup_db import db
from config import Config
from flask_migrate import Migrate


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config.from_envvar("APP_SETTINGS", silent=True)
    app.json.ensure_ascii = False
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)


app = create_app(Config())


@app.route("/", methods=["POST", "GET"])
def posts_all():
    try:
        posts_all = get_posts_all()
        if len(posts_all) == 0:
            return "", 404
        pa = request.form.get("pa")
        em = request.form.get("em")
        if bool(pa) * bool(em):
            user = user_service.get_email(em)
            if user_service.compare_passwords(user.password, pa):
                return render_template("index.html", user=user.name, posts_all=posts_all, len=len(posts_all))
        return render_template("index.html", user=None, posts_all=posts_all, len=len(posts_all))
    except FileNotFoundError:
        return "серверы недоступны", 500
    except:
        return "возможна ошибка шаблона", 500


@app.route("/search/")
def search():
    try:
        g = request.args.get("s")
        posts = search_for_posts(g)
        if len(posts) == 0:
            return "", 404
        return render_template("search.html", posts=posts, lener=len(posts))
    except FileNotFoundError:
        return "серверы не доступны", 500
    except:
        return "возможна ошибка шаблона", 500


@app.route("/posts/<int:post_id>")
def posts(post_id):
    try:
        post_id = int(post_id)
        post = get_post_by_pk(post_id)
        if len(post) == 0:
            return "", 404
        comments = get_comments_by_post_id(post_id)
        return render_template("post.html", post=post, comments=comments, lener=comments_endings(len(comments)))
    except FileNotFoundError:
        return "серверы не доступны", 500
    except:
        return "возможна ошибка шаблона", 500


@app.route("/users/<username>")
def user_feed(username):
    try:
        posts = get_posts_by_user(username)
        if len(posts) == 0:
            return "", 404
        return render_template("user-feed.html", posts=posts)
    except FileNotFoundError:
        return "серверы не доступны", 500
    except:
        return "возможна ошибка шаблона", 500


@app.route("/registration/")
def get_registration():
    return render_template("registration.html")


@app.route("/create_user/", methods=["POST"])
def create_user():
    lo = request.form.get("lo")
    pa = request.form.get("pa")
    em = request.form.get("em")
    if bool(lo) * bool(pa) * bool(em):
        reg = user_service.register(em, pa, lo)
        if reg:
            return render_template("create_user.html", user=lo)
    return render_template("not_create_user.html")


@app.route("/created_user/", methods=["POST"])
def created_user():
    return render_template("authorization.html")

migrate = Migrate(app, db, render_as_batch=True)

if __name__ == "__main__":
    app.run()

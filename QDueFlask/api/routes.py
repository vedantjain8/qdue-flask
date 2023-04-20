from flask import Blueprint, request, abort
from QDueFlask.models import Todo, User
from QDueFlask import app_logger

apis = Blueprint("apis", __name__, url_prefix="/api")

@apis.route('/', methods=['GET'])
def api():
    app_logger.warning('Request received: %s %s for apiKey %s', request.method, request.url, apikey)
    apikey = request.args.get('api')
    try:
        userid = (User.query.filter_by(api=apikey).first()).id
        allPosts = Todo.query.filter_by(user_id=userid).all()
        posts = []
        for count in range(Todo.query.filter_by(user_id=userid).count()):
            posts.append(str(str(allPosts[count]).split("><:SPLITFROMHERE:><")))
        return posts
    except:
        app_logger.warning('Request received: %s %s for apiKey %s', request.method, request.url, apikey)
        abort(404)
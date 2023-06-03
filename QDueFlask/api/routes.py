from flask import Blueprint, request, abort
from QDueFlask.models import Todo, User
from QDueFlask import app_logger

apis = Blueprint("apis", __name__, url_prefix="/api")

@apis.route('/', methods=['GET'])
def api():
    apikey = request.args.get('api')
    app_logger.info('Request received: %s %s for apiKey %s', request.method, request.url, apikey)
    try:
        userid = (User.query.filter_by(api=apikey).first()).id
        allPosts = Todo.query.filter_by(user_id=userid).all()
        totalPostCount = Todo.query.filter_by(user_id=userid).count()
        posts = []
        for count in range(totalPostCount):
            posts.append(str(allPosts[count]))
        return posts
    except:
        app_logger.warning('Request received: %s %s for apiKey %s, Returned with 404', request.method, request.url, apikey)
        abort(404)
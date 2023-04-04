from flask import Blueprint, request
from flaskblog.models import Todo, User

apis = Blueprint("apis", __name__, url_prefix="/api")

@apis.route('/', methods=['GET'])
def api():
    apikey = request.args.get('api')
    userid = (User.query.filter_by(api=apikey).first()).id
    allPosts = Todo.query.filter_by(user_id=userid).all()
    posts = []
    for count in range(Todo.query.filter_by(user_id=userid).count()):
        posts.append(str(str(allPosts[count]).split("><:SPLITFROMHERE:><")))
    return posts
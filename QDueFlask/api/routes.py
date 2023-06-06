from flask import Blueprint, request, abort, jsonify
from QDueFlask.models import Todo, User
from QDueFlask import app_logger, customTZ
from flask_login import current_user
from datetime import datetime, timedelta

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


@apis.route('/update_activity', methods=['POST'])
def update_activity():
    if current_user.is_authenticated:
        current_user.update_activity()
        return 'Activity updated', 200
    return 'Activity updated', 200

@apis.route('/get_active_users')
def get_active_users():
    # Calculate current time
    current_time = datetime.now(customTZ)

    # Filter active users (last_activity within the last 5 minutes)
    active_users = User.query.filter(User.last_activity > current_time - timedelta(minutes=5)).all()

    # Return active users as JSON response
    active_users_list = [user.username for user in active_users]
    return jsonify(active_users_list), 200
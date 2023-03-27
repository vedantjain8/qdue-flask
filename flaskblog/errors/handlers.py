from flask import Blueprint, render_template
from random import choice

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(404)
def error_404(error):
    error_line= ["Looks like you took a wrong turn at Albuquerque.",
"We can't seem to find what you're looking for. Maybe try looking in the fridge?",
"This page is like a unicorn - it doesn't exist.",
"Oops, it looks like we've lost this page in the interwebs.",
"404 error: Page not found. But don't worry, we're still here for you, even if the page isn't.",
"We're sorry, but the page you're looking for has vanished into the ether.",
"We couldn't find the page you were looking for. Maybe it's hiding behind the couch?",
"404 error: Page not found. But hey, at least you found us!"]
    return render_template('errors/404.html', error_line= choice(error_line), errorCode = 404), 404


@errors.app_errorhandler(403)
def error_403(error):
    error_line = ["It looks like you're not allowed to see this page. Sorry, no sneaking past the bouncer.",
"We're sorry, but you're not authorized to access this page. Maybe try asking your cat for the password?",
"403 error: Access denied. But hey, at least you tried.",
"We couldn't let you see this page. It's top secret, and only available to agents with level 10 clearance or higher.",
"It looks like you don't have the proper clearance to view this page. Sorry, no unauthorized access allowed.",
"We're sorry, but this page is off-limits. Maybe try your luck with another page?",
"403 error: Access denied. But don't worry, there are plenty of other pages you're allowed to see.",
"Sorry, but you don't have permission to access this page. Better luck next time!"]
    return render_template('errors/404.html', error_line= choice(error_line), errorCode = 403), 403


@errors.app_errorhandler(500)
def error_500(error):
    error_line= ["Looks like something went wrong on our end. Sorry about that!",
"Oops, it looks like we broke the internet. Sorry about the inconvenience.",
"We're sorry, but something has gone awry on our end. But don't worry, we'll have it fixed in no time.",
"500 error: Something has gone horribly, horribly wrong. But hey, at least you're not alone - we're just as confused as you are.",
"It looks like something has gone wrong on our end. Maybe try unplugging the internet and plugging it back in again?",
"We're sorry, but it looks like something has gone awry. Maybe try coming back later and hoping for the best?",
"500 error: Something has gone terribly wrong. But don't worry, we're working on it. In the meantime, try not to panic.",
"It looks like something has gone wrong on our end. Sorry about that! We'll have it sorted out as soon as we can."]
    return render_template('errors/404.html', error_line= choice(error_line), errorCode = 500), 500
from flaskblog import app,db

if __name__=="__main__":
    app.app_context().push()
    db.create_all()
    # app.debug=True
    app.run(host='0.0.0.0', port=80)
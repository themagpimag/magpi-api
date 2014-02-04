from app import app
import flask

@app.route('/issues/<id>')
def get_issue(id):
    issue = get_issue_from_db(id)
    return flask.jsonify(issue)

@app.route('/issues')
def get_issues():
    issue = get_issues_list_from_db()
    return flask.jsonify(issue)

def get_issue_from_db(issue):
    pass

def get_issues_list_from_db():
    pass
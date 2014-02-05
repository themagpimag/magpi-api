from app import app
from issue import Issue
import flask, requests, json
import logging

@app.route('/issues/<id>')
def get_issue(id):
    id = int(id)
    issue = get_issue_from_db(id)
    if issue:
        return flask.jsonify(issue), 200
    else:
        return flask.jsonify( { 'error' : 'not found' } ) , 404

@app.route('/issues')
def get_issues():
    issues_list = get_issues_list_from_db()
    if issues_list:
        return flask.jsonify( issues_list ), 200
    else:
        return flask.jsonify( { 'error' : 'not found' } ) , 404

def get_issue_from_db(issue):
    issues = Issue.query(Issue.id==issue).fetch()
    if issues:
        return issues[0].maximize()
    return None

def get_issues_list_from_db():
    issues = Issue.query().fetch()
    if issues:
        issues_list = {}
        issues_list['issues'] = []
        for issue in issues:
            issues_list['issues'].append(issue.minimize())
        return issues_list
    return None

@app.route('/sync_issues')
def sync_issues():
    req = requests.get('http://www.themagpi.com/mps_api/mps-api-v1.php?mode=list_issues')
    old_issues = json.loads(req.text)
    if not 'data' in old_issues:
        return flask.jsonify( { 'error' : 'empty data from MagPi' } ) , 500
    for old_issue in old_issues['data']:
        issue = Issue(key=Issue.generate_key(old_issue['title']))
        issue.fill_from_old(old_issue)
        issue.put()
    return flask.jsonify( { 'status' : 'sync done' } ), 200
    
from app import app
from models.issue import Issue
from models.news import News
import flask, requests, json
import logging, feedparser
from google.appengine.datastore.datastore_query import Cursor

@app.route('/issues/<id>')
def get_issue(id):
    if not id.isdigit():
        return flask.jsonify( 
            { 'error' : 'bad parameter, an integer is required' } ) , 400
    id = int(id)
    issue = get_issue_from_db(id)
    if issue:
        return flask.jsonify(issue), 200
    else:
        return flask.jsonify( { 'error' : 'not found' } ) , 404

@app.route('/issues')
def get_issues():
    issues_list = get_issues_list_from_db(flask.request.args.get('pagetoken'))
    if issues_list:
        return flask.jsonify( issues_list ), 200
    else:
        return flask.jsonify( { 'error' : 'not found' } ) , 404

@app.route('/news')
def get_news():
    news_list = get_news_list_from_db(flask.request.args.get('pagetoken'))
    if news_list:
        return flask.jsonify( news_list ), 200
    else:
        return flask.jsonify( { 'error' : 'not found' } ) , 404

def get_issue_from_db(issue):
    issues = Issue.query(Issue.id==issue).fetch()
    if issues:
        return issues[0].maximize()
    return None

def get_issues_list_from_db(token):
    curs = Cursor(urlsafe=token)
    issues, curs, _ = Issue.query().order(-Issue.id).fetch_page(10, start_cursor=curs)
    if issues:
        issues_list = {}
        if curs:
            issues_list['pagetoken'] = curs.urlsafe()
        issues_list['issues'] = []
        for issue in issues:
            issues_list['issues'].append(issue.minimize())
        return issues_list
    return None

def get_news_list_from_db(token):
    curs = Cursor(urlsafe=token)
    newss, curs, _ = News.query().order(-News.date).fetch_page(10, start_cursor=curs)
    if newss:
        newss_list = {}
        if curs:
            newss_list['pagetoken'] = curs.urlsafe()
        newss_list['news'] = []
        for news in newss:
            newss_list['news'].append(news.maximize())
        return newss_list
    return None

@app.route('/sync_issues')
def sync_issues():
    req = requests.get('http://www.themagpi.com/mps_api/mps-api-v1.php?mode=list_issues')
    old_issues = json.loads(req.text)
    if not 'data' in old_issues:
        return flask.jsonify( { 'error' : 'empty issue data from MagPi' } ) , 500
    for old_issue in old_issues['data']:
        issue = Issue(key=Issue.generate_key(old_issue['title']))
        issue.fill_from_old(old_issue)
        issue.put()
    return flask.jsonify( { 'status' : 'issues sync done' } ), 200

@app.route('/sync_news')
def sync_news():
    feed = feedparser.parse("http://feeds.feedburner.com/TheMagPiNews")
    old_newss = feed['items']
    if not old_newss:
        return flask.jsonify( { 'error' : 'empty news data from MagPi' } ) , 500
    for old_news in old_newss:
        news = News(key=News.generate_key(old_news['title']))
        news.fill_from_old(old_news)
        news.put()
    return flask.jsonify( { 'status' : 'news sync done' } ), 200
    
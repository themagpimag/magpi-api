import os, sys
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'flaskstuff'))
from flask import Flask

app = Flask(__name__)
from app import views

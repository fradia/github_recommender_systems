from flask import Flask, request, render_template, jsonify
import sqlite3
import json


# Setup Flask app
app = Flask(__name__)


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('index_2.html')

@app.route('/compute_ur')
def compute_ur():
    userInput = request.args.get('userInput')
    conn = sqlite3.connect('database_reccom.db')
    c=conn.cursor()
    t = (userInput,)
    result=dict()
    for x,y,z in c.execute('SELECT * FROM ur_rec WHERE name=?',t):
        l=json.loads(y)
        s=json.loads(z)
        if len(l)==0:
            result={'links':['no_result'],'scores':['no_score']}
        else:
            result={'links':l['links'],'scores':s['scores']}
    return jsonify(result)


@app.route('/compute_als')
def compute_als():
    userInput = request.args.get('userInput')
    conn = sqlite3.connect('database_reccom.db')
    c=conn.cursor()
    t = (userInput,)
    result=dict()
    for x,y,z in c.execute('SELECT * FROM als_rec WHERE name=?',t):
        l=json.loads(y)
        s=json.loads(z)
        if len(l)==0:
            result={'links':['no_result'],'scores':['no_score']}
        else:
            result={'links':l['links'],'scores':s['scores']}
    return jsonify(result)
    
# Main
if __name__ == "__main__":
    app.run(debug=True)

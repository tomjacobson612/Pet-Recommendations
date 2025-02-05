"""
Dog breed recommendation app. Detects dog breed via user provided photo and gives care recommendations.
"""
import flask
import os
from query import Query; from results import Results;

app = flask.Flask(__name__) 

app.add_url_rule('/', view_func=Query.as_view('query'), methods=['GET', 'POST'])

app.add_url_rule('/results', view_func=Results.as_view('results'), methods=['GET'])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
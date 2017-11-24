import sys
import sqlite3

from flask import Flask, jsonify, request
from flask import render_template

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TESTING'] = True
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True




DATABASE = "../recruit.db"

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def query_db(query):

    result_dict = {}

    try:
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute(query)
        result_dict = dictfetchall(cursor)

    except sqlite3.OperationalError as e:
        print("Db operation error", e)
        result_dict["error"] = str(e)
    except:
        e = sys.exc_info()[0]
        print("An error occurred with the database", e)
        result_dict["error"] = str(e)
    else:
        cursor.close()
        connection.close()

    return result_dict


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/query', methods=['GET'])
def query():
    print("--------------------------------------------------------------")
    print("- START -")
    print("--------------------------------------------------------------")
    q = request.args.get('q', '')
    print(q)
    result_dict = query_db(q)
    print("**************************************************************")
    print(result_dict)
    print("--------------------------------------------------------------")
    print("- FINISH -")
    print("--------------------------------------------------------------")
    print(".")
    print(".")
    print(".")
    return jsonify({'data': result_dict})

if __name__ == '__main__':
    app.run()

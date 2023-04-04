from flask import Flask, render_template, request
import sqlite3
import os

print(os.getcwd())

dbPath = 'file:./database/database.db?mode=ro'

app = Flask(__name__)

@app.route('/')
def show_home():
    return render_template("index.html")

@app.route('/getAllGenre', methods=["POST"])
def searchBy():
    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()
    cursor.execute('select distinct genre from genres')
    
    genres = list()

    for g in cursor.fetchall():
        genres.append(g[0])
    
    conn.close()
    return genres




@app.route('/getAll/<varb>', methods=['POST'])
def test(varb):
    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()

    try:
        result = list()
        res = cursor.execute(f" select * from {varb}")
        names = [description[0] for description in cursor.description]
    
        if res.fetchone() is not None:
            result.append(names)
            for r in res.fetchall():
                result.append(r)
        else:
            result =  ['No result found']

    except:
        result =  ['No result found'] , 400
    
    return result


def readInput(input):
    data = input.split('+')
    for i in range(len(data)):
        data[i] = tuple(data[i].split('='))
    return data




app.run(debug=True,port=2780)
print("\nprogram execution complete!")
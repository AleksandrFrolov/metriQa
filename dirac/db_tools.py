import sqlite3 as sql

def fragments_db(data):
    try:
        connect = sql.connect('./fragment.db')
    except sql.Error:
        print 'Error database connect...'
    with connect:
        cursor = connect.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS fragments (f_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, smiles TEXT, type TEXT);")
        for fragment in data:
            name = fragment.name
            smiles = fragment.smiles
            type = fragment.type
            cursor.execute("SELECT * FROM fragments WHERE name=? and smiles=?;", (name, smiles))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO fragments VALUES(?, ?, ?, ?);", (None, name, smiles, type))

def fragments_view():
    try:
        connect = sql.connect('./fragment.db')
    except sql.Error:
        print 'Error database connect...'
    with connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM fragments;")
        return cursor.fetchall()
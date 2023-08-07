from flask import request, jsonify
import sqlite3
from sqlite3 import Error
from fuzzywuzzy import fuzz, process


def save(app):

    @app.route('/save', methods=['POST'])
    def save_query():
        conn = create_connection()
        if conn is not None:
            cur = conn.cursor()
            shortName = request.json['shortName']
            question = request.json['question']
            data = request.json['data']
            rawdata = request.json['globalData_string']
            columnnames = request.json['globalCols_string']

            if data is not None:
                try:
                    cur.execute("INSERT INTO entries (shortName, question, data, rawdata, columnnames) VALUES ( ?, ?, ?, ?, ?)", (shortName, question, data, rawdata, columnnames))
                    conn.commit()

                    return jsonify({ 'message': 'Data saved successfully.'}), 200
                
                except Error as e:
                    print(e)
                    return jsonify({ 'error': 'Failed to save the data.'}), 500
            else:
                return 'No result to be saved', 400
            


def data(app):

    @app.route('/data', methods=['GET'])
    def get_data():
        conn = create_connection()
        if conn is not None:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id, shortName, question, data, rawdata, columnnames FROM entries")
                rows = cur.fetchall()
                col_names = [description[0] for description in cur.description]
                entries = [dict(zip(col_names, row)) for row in rows]

                return jsonify(entries), 200
            
            except Error as e:
                print(e)
                return jsonify({'error': 'Failed to fetch data'}), 500



def delete(app):

    @app.route('/data/delete', methods=['POST'])
    def delete_row():
        try:
            row_id = request.json.get('rowId')
            if not row_id:
                return jsonify({'error': 'rowId parameter is missing.'}), 400

            conn = create_connection()
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM entries WHERE id = ?", (row_id,))
                conn.commit()
                conn.close()
                return jsonify({'message': f'Row with id {row_id} has been deleted successfully.'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500




def cache(app):

    @app.route('/cache', methods=['POST'])
    def cache_search():
        try:
            query = request.json['query']
            if not query:
                return jsonify({'error': 'rowId parameter is missing.'}), 400

            conn = create_connection()
            if conn is not None:
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM entries")
                rows = cursor.fetchall()

                max_ratio = 0
                max_row = None

                for row in rows:
                    question = row['question']
                    ratio = fuzz.ratio(query.lower, question.lower())
                    if ratio > max_ratio:
                        max_row = row

                if max_ratio > 85:
                    return jsonify({'match': True, 'row': max_row}), 200
                else:
                    return jsonify({'match': False, 'row': None}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('savedQueries.db')
        print('Connected to the savedQueries database')
    except Error as e:
        print(e)

    return conn





































from flask import request
from dotenv import load_dotenv
load_dotenv()
import sqlite3

from gpt import get_text


def sql(app):

    @app.route('/sql/query', methods=['POST'])
    def sql_query():

        try:
            index = int(request.get_json()['databaseValue'])
            database_names = ['cgdb.sqlite', 'cvd.db', 'sleep.db']
            db_name = database_names[index] 
            query = request.get_json()['query']
            sql = request.get_json()['sql']
            connection = sqlite3.connect(db_name)
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()

            col_names=[i[0] for i in cursor.description]
            no_of_cols=get_column_count(rows)
            no_of_rows=get_row_count(rows)

            """ If there's only one row of output, then convert into into a sentence"""
            if (no_of_rows == 1 or no_of_cols == 1):
               text = get_text(cols_and_data="Question: " + query + ", Columns:" + ",".join(str(x) for x in col_names) + ", Data:" + ",".join(str(x) for x in rows))
               return {
                  "status": 'success',
                  "type": 'text',
                  "data": text,
               }
            else:
              return {
                "status": 'success', 
                "type": 'table',
                "data": rows, 
                "columnNames": col_names,
                "noOfColumns": no_of_cols, 
                "noOfRows": no_of_rows, 
               }

        except Exception as e:
            return {"status": 'error', "message": "Error: " + str(e)}

def get_row_count(sql_output):
  """Returns the number of rows in the SQL output."""
  row_count = 0
  for row in sql_output:
    row_count += 1
  return row_count

def get_column_count(sql_output):
  """Returns the number of columns in the SQL output."""
  column_count = 0
  for row in sql_output:
    column_count = max(column_count, len(row))
  return column_count

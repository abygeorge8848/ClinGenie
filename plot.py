from flask import Flask, request, make_response
from flask_cors import CORS
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
import json
import io
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.environ["OPENAI_API_KEY"] = "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"

app = Flask(__name__)
CORS(app)

try:
    db = SQLDatabase.from_uri("sqlite:///.\\cgdb.sqlite")
except Exception as e:
    print(f"Error connecting to the database: {str(e)}")

llm = OpenAI(temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_direct=True, use_query_checker=True, return_intermediate_steps=True)

@app.route('/plot', methods=['POST'])
def plot():
    try:
        query = request.json.get('query')  # Extract the query from the request JSON
        print(f"Charlie and his bucketfull of dinosaurs: {query}")
 
        prompt = f"Provide the python code, using seaborn, pandas, matplotlib, or scipy, or any appropriate combination of the aforementioned libraries to plot the data on the most appropriate chart for this data: {json.dumps(query)}"
          # Run the query through the db_chain
        result = db_chain(prompt)
        print(f"yello bro whaddup, {llm(prompt)}")
        exec(llm(prompt), {})

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        #plt.show()
        buffer.seek(0)

        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'image/png'
        return response

    except Exception as e:
        print(f"Error occurred during plot generation: {str(e)}")

if __name__ == '__main__':
    app.run(port=5000)

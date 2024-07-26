from flask import Flask, render_template, jsonify
import json
from modules.db_reader import query_df, job_data_with_id

app = Flask(__name__)
json_path = r'temp/emp_data.json'


def job_data():
    with open('modules/query.txt', 'r') as f:
        query = f.read()
    data = query_df(query)
    # print(data)
    return data


# job_data()

@app.route('/')
def hello_world():
    return render_template("home.html", jobs=job_data(), len=len(job_data()))


@app.route('/api/jobs')
def list_jobs():
    data = job_data()
    json_data = data.to_json(orient='records')
    json_data = json.loads(json_data)
    return jsonify(json_data)


@app.route('/job/<id>')
def show_job(id):
    data = job_data_with_id(id)
    return jsonify(json.loads(data.to_json(orient='records')))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

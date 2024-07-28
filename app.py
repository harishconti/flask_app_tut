from flask import Flask, render_template, jsonify, request
import json
from modules.db_reader import query_df, job_data_with_id, add_application_db

app = Flask(__name__)
json_path = r'temp/emp_data.json'


def job_data():
    with open('modules/query.txt', 'r') as f:
        query = f.read()
        # print(query)
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
    data = json.loads(data.to_json(orient='records'))
    if not data:
        # return jsonify({'error': 'No such job'}), 404
        return "Not Found", 404
    return render_template('jobpage.html', jobs=data)


@app.route('/job/<id>/apply', methods=['GET', 'POST'])
def apply_job(id):
    if request.method == 'POST':
        data = request.form.to_dict()  # Use request.form for POST data
        job = job_data_with_id(id)
        add_application_db(id, data)
        # print(data)
        return render_template('application_submitted.html', application=data, job=job)
    else:  # GET request
        return render_template('application_form.html', job_id=id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

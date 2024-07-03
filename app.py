from flask import Flask, render_template
import json

app = Flask(__name__)
json_path = r'temp/emp_data.json'


def json_data(path):
    with open(path) as data_file:
        data = json.load(data_file)['jobs']
    return data


@app.route('/')
def hello_world():
    return render_template("home.html", jobs=json_data(json_path))


@app.route('/api/jobs')
def list_jobs():
    return json_data(json_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

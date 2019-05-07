from flask import Flask, redirect, send_file
from flask_restful import Api
import os

app = Flask(__name__)
current_dir = os.getcwd

@app.before_request
def clear_json():
    os.system('rm tmp/*')

@app.route("/v1")
def index():
    return redirect("https://sileogen.com")

@app.route("/v1/download/<json_name>")
def return_files(json_name):
    return send_file('tmp/{}.json'.format(json_name), attachment_filename='{}.json'.format(json_name))

api = Api(app)

from app import resources

api.add_resource(resources.Generate, '/v1/generate')
api.add_resource(resources.Shield, '/v1/shield')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

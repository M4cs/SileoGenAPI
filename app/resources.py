from flask import redirect, request, send_file, make_response, jsonify
from flask_restful import Resource, reqparse
from app import app
from app.helper import SileoGenerator
import json

def generate_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('title')
    parser.add_argument('author')
    parser.add_argument('version')
    parser.add_argument('short_description')
    parser.add_argument('long_description')
    parser.add_argument('screenshots')
    return parser

class Generate(Resource):
    def post(self):
        data = request.form.to_dict(flat=False)
        response = make_response()
        title = data['title'][0]
        author = data['author'][0]
        version = data['version'][0]
        price = data['price'][0]
        summary = data['summary'][0]
        long_description = data['long_description'][0]
        screenshots = data['screenshots'][0]
        headerImage = data['headerImage'][0]
        generator = SileoGenerator(title, summary, author, long_description, version, headerImage, price, screenshots)
        generator.generate_template()
        with open('app/count.json', 'r+') as json_file:
            obj = json.load(json_file)
            obj['count'] += 1
            json_file.seek(0)
            json.dump(obj, json_file, indent=4)
            json_file.truncate()
            json_file.close()
        return send_file('../tmp/{}.json'.format(generator.title), attachment_filename="{}.json".format(generator.title), as_attachment=False)

class Shield(Resource):
    def get(self):
        with open('app/count.json', 'r+') as json_file:
            obj = json.load(json_file)
            count = obj['count']
            json_file.close()
        return jsonify({ "schemaVersion": 1,
                 "label": "Depictions Generated:",
                 "message": str(count),
                 "color": "blue"
               })

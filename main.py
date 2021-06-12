from flask import Flask, redirect, url_for
from flask_restful import Resource, Api, reqparse, abort
from random import randInt

app = Flask(__name__)
api = Api(app)

boxes = {}

class addItem (Resource):

    def get(self, item):
        box[item] = randInt(0,1)
        return box[item], 201



api.add_resource(addItem, "/item/add")

if __name__ == '__main__':
    app.run(debug=True)
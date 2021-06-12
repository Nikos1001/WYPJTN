from os import stat
from flask import Flask, redirect, url_for, render_template
from flask_restful import Resource, Api, reqparse, abort
from random import randint
import requests

app = Flask(__name__, '/static')
api = Api(app)

boxes = {}

curr_item = 'shoe'
curr_box = 0

# curr_box = 1 - curr_box
def turn_on(box_id):
  print(str(box_id) + ' on')
  requests.get('http://192.168.1.11' + str(box_id) + '/on')

def turn_off(box_id):
  print(str(box_id) + ' off')
  requests.get('http://192.168.1.11' + str(box_id) + '/off')

class addItem (Resource):
  def get(self, item):
    global curr_box, curr_item
    print(item)
    curr_item = item
    curr_box = randint(0,1)
    turn_on(curr_box)
    boxes[curr_item] = curr_box
    return {curr_item: curr_box}, 200

class boxFull (Resource):
  def get(self):
    global curr_box, curr_item
    turn_off(curr_box)
    #global curr_box?????????
    if curr_box == 0:
      curr_box=1
    else:
      curr_box=0
    turn_on(curr_box)
    return '', 204

class itemConfirm (Resource):
  def get(self):
    global curr_box, curr_item
    turn_off(curr_box)
    boxes[curr_item] = curr_box
    return boxes[curr_item], 201

class findItem (Resource):
  def get(self, item):
    global curr_box, curr_item
    if item in boxes:
      turn_on(boxes[item])
      return boxes[item], 201
  
class remove (Resource):
  def get(self, item):
    global curr_box, curr_item
    if item in boxes:
      turn_off(boxes[item])
      boxes.pop(item)
      return "removed item", 200
    else:
        abort(404, message = "not found")

class listItems (Resource):
  def get(self):
    output = {}
    for i in boxes:
      output[boxes[i]].append(i)
    return output
      

@app.route('/aaa')
def my_site():
    return render_template('home.html')


api.add_resource(addItem, "/item/add/<string:item>")
api.add_resource(boxFull, "/box/full")
api.add_resource(itemConfirm, "/item/confirm")
api.add_resource(findItem, "/item/find/<string:item>")
api.add_resource(remove, "/item/remove/<string:item>")
api.add_resource(listItems, "/item/list")

if __name__ == '__main__':
    app.run(debug=True)
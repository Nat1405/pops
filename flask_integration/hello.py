from flask import Flask, request, jsonify
app = Flask(__name__)


safeZone = {safeZone: [ [2.29452158, 59.14978110], [10.12683778, 56.53733116], [14.1772154, 60.7167403], [21.45396446, 60.23528403], [28.59885697, 63.67010079] ]}


@app.route('/')
def hello_world():
    return 'Hey there!'

@app.route('/planning')
def planning():
    return jsonify(safeZone)

from Cities import NearbyCites
from flask import Flask
from flask import request 

app = Flask(__name__)

@app.route('/')
def getData():
    city = request.args.get("city")
    state = request.args.get("state")
    country = request.args.get("country")
    key = request.args.get("key")

    if key == "7295":
        print('Getting data.')
        data = NearbyCites().Cities(city,state,country)
        return data
    else:
        return [{'Invalid: Key'}]

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
from Cities import NearbyCites
from flask import Flask
from flask import request 

app = Flask(__name__)

@app.route('/')
def getData():
    city = request.args.get("city")
    state = request.args.get("state")
    country = request.args.get("country")

    print('Getting data.')
    data = NearbyCites().Cities(city,state,country)
    return data

if __name__ == '__main__':
    app.run()
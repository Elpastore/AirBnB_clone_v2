#!/usr/bin/python3
"""
    starts a Flask web application:
"""
from flask import Flask, render_template
# from models.state import State
from models import *
from models import storage

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    fetching data from the storage engine
    """
    states_list = storage.all("State").values()
    return render_template('8-cities_by_states.html', states=states_list)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

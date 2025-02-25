#!/usr/bin/python3
"""
    starts a Flask web application:
"""
from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    fetching data from the storage engine
    """
    states_list = storage.all("State").values()
    # sorted_states = sorted(list(states_list), key=lambda state: state.name)
    return render_template('7-states_list.html', states=states_list)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

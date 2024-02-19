#!/usr/bin/python3
"""
    starts a Flask web application:
"""
from flask import Flask, render_template
# from models.state import State
from models import *
from models import storage

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def filters():
    """
    fetching data from the storage engine
    """
    # Let's import the values of dict
    states_list = storage.all("State").values()
    amenities_list = storage.all("Amenity").values()
    # sorted_states = sorted(list(states_list), key=lambda state: state.name)
    return render_template('10-hbnb_filters.html', states=states_list, amenities=amenities_list)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

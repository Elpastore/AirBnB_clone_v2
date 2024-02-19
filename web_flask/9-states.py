#!/usr/bin/python3
"""
    starts a Flask web application:
"""
from flask import Flask, render_template
# from models.state import State
from models import *
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def states(state_id=None):
    """
    fetching data from the storage engine
    """
    # Let's import the dict
    states_list = storage.all("State")
    if state_id:
        state_id = 'State.' + state_id
    # sorted_states = sorted(list(states_list), key=lambda state: state.name)
    return render_template('9-states.html', states=states_list,
                           state_id=state_id)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

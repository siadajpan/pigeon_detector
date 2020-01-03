from flask import Flask, jsonify

import settings
from movement_controller.movement_controller import MovementController


movement_controller = MovementController()
app = Flask(__name__)


@app.route(settings.Server.MOVEMENT, methods=['POST'])
def start_movement():
    movement_controller.start_movement()
    return jsonify(True)


app.run(host='0.0.0.0', port=5000)

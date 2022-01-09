import numpy as np
from app.base.APIResponse import APIResponse
from app.weather import weather_bp
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_restful import Api


class SpecialFlask(Flask):
    
    def make_response(self, rv):
        if isinstance(rv, (list, dict, np.ndarray)):
            res = APIResponse(rv)
            return jsonify(res.body())
        return super().make_response(rv)

def create_app():
    app = SpecialFlask(__name__)
    api = Api(app)
    CORS(app)
    
    app.register_blueprint(weather_bp, url_prefix='/weather')
    return app
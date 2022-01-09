from . import weather_bp
import json

from app.utils.dateutil import parse_ymd
from flask import request
from flask_cors import cross_origin

from . import weather_bp
from .api.WeatherApi import request_weather_info


class Weather:
    
    @cross_origin()
    @weather_bp.route('/get_weather_info_between')
    def get_weather_info_between():
        
        city_id = int(request.args.get('cityId'))
        startDate = parse_ymd(request.args.get('startDate'))
        endDate = parse_ymd(request.args.get('endDate'))
        
        result = request_weather_info(city_id, startDate, endDate, df=True)
        parsed = json.loads(result)
        print(type(parsed))
        # return json.dumps(parsed, indent=4)
        return parsed
        
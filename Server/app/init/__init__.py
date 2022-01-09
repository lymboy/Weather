import json
import os

import numpy as np
from flask import Flask, jsonify, current_app, make_response, Response
from flask_cors import CORS
from flask_restful import Api
from six import PY3


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        
        print("\n\n\n测试测试测试\n\n\n")
        
        if isinstance(response, np.ndarray):
            response = jsonify(response.tolist())
        if isinstance(response, (list, dict)):
            response = jsonify(response)
        return super(Response, cls).force_type(response, environ)

class MyFlask(Flask):
    response_class = JsonResponse

def create_app(test_config=None):
    # create and configure the app
    # app = MyFlask(__name__, instance_relative_config=True)
    app = Flask(__name__)
    app.response_class = JsonResponse
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    api = Api(app)
    CORS(app, supports_credentials=True)

    @api.representation('application/json')  # 指定响应形式对应的转换函数
    def output_json(data, code, headers=None):
        """自定义json形式"""
        # 根据flask内置配置, 进行格式处理(缩进/key是否排序等)
        settings = current_app.config.get('RESTFUL_JSON', {})

        if current_app.debug:
            settings.setdefault('indent', 4)
            settings.setdefault('sort_keys', not PY3)

        # 添加json外层包装
        if 'message' not in data:  # 判断是否设置了自定义的错误信息
            data = {
                'code': code,
                'message': 'ok',
                'data': data
            }

        # 字典转json字符串
        dumped = json.dumps(data, **settings) + "\n"

        # 构建响应对象
        resp = make_response(dumped, code)
        resp.headers.extend(headers or {})
        return resp

    return app
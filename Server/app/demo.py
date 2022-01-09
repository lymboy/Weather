from json import dumps

from flask import Flask, current_app, make_response
from flask_restful import Resource, Api
from six import PY3

app = Flask(__name__)
api = Api(app)


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
    dumped = dumps(data, **settings) + "\n"

    # 构建响应对象
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


class DemoResource(Resource):
    def get(self):

        return {'foo': "get"}

    def post(self):
        return {'message': 'parameter error: name', "data": None}

api.add_resource(DemoResource, '/')

if __name__ == '__main__':
    app.run(debug=True)


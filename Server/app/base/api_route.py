from functools import wraps

from flask import jsonify

from .APIResponse import APIResponse


def route(bp,*args,**kwargs):
    def decorator(f):
        @bp.route(*args,**kwargs)
        @wraps(f)
        def wrapper(*args,**kwargs):
            result = f(*args,**kwargs)
            res = APIResponse(result)
            return jsonify(res.body())
        return f
    return decorator
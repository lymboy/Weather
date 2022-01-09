import numpy as np
class APIResponse():
    msg='ok'
    error=0
    data={}

    def __init__(self,data,msg='ok',error=0):
        if msg:
            self.msg=msg
        if isinstance(data, np.ndarray):
            data = data.tolist()
        self.data=data

    def body(self):
        body={}
        body['data']=self.data
        body['msg']=self.msg
        body['code']=self.error

        return body
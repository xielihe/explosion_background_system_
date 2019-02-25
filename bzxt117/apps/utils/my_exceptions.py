from rest_framework.views import exception_handler


def custom_exception_handler(exc,context):
    response = exception_handler(exc,context) #获取本来应该返回的exception的response
    if response is not None:
        #response.data['status_code'] = response.status_code  #可添加status_code
        response.data['message'] = response.data['detail']    #增加message这个key
        del response.data['detail']  #删掉原来的detail
    return response
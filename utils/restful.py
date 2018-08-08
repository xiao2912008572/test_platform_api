from flask import jsonify


# http状态码 - 转code码
class HttpCode(object):
    get_ok = 200
    post_ok = 201
    put_ok = 204
    delete_ok = 200
    unautherror = 403
    paramerror = 400
    servererror = 500


# 对jsonify进行封装，传入code，message，data
def restful_result(code, message, data):
    '''
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return jsonify(
        {
            'code': code,
            'message': message,
            'data': data or {}
        }, code
    )


def success(message=None, data=None, methods=None):
    '''
    成功 200
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    if methods == 'get':
        return restful_result(code=HttpCode.get_ok, message=message, data=data)
    elif methods == 'post':
        return restful_result(code=HttpCode.post_ok,message=message,data=data)
    elif methods == 'delete':
        return restful_result(code=HttpCode.delete_ok,message=message,data=data)
    elif methods == 'put':
        return restful_result(code=HttpCode.put_ok,message=message,data=data)


def unauth_error(message=''):
    '''
    未授权 401
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return restful_result(code=HttpCode.unautherror, message=message, data=None)


def params_error(message=''):
    '''
    参数错误 400
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return restful_result(code=HttpCode.paramerror, message=message, data=None)


def server_error(message=''):
    '''
    服务器错误 500
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return restful_result(code=HttpCode.servererror, message=message or '服务器内部错误', data=None)

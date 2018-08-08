# Author:Xiaojingyuan

from exts import db
from flask import Blueprint, session, url_for, render_template, views, request, jsonify
from flask_restful import Api, Resource, fields, marshal_with, abort, reqparse, inputs
from models import EoApiEnv, EoProject, EoApiEnvParam, EoApiEnvAdditionalParam, EoApiEnvHeader, EoApiEnvFrontUri

env_bp = Blueprint('env', __name__, url_prefix='/api/v1/env')
api = Api(env_bp)  # 使用蓝图注册api


# 404操作
def abort_if_todo_doesnt_exist(env_id):
    if EoApiEnv.query.filter_by(envID=env_id).first() == None:
        abort(404, message='ID={0}的资源不存在!'.format(env_id))


def abrot_if_todo_doesnt_exist_project(project_id):
    if EoProject.query.filter_by(projectID=project_id).first() == None:
        abort(404, message='ID={0}的资源不存在!'.format(project_id))


# 环境详情
class Env(Resource):
    resource_fields_get = {
        'envName': fields.String,
        'envDesc': fields.String,
        'uri': fields.Nested({
            'uri': fields.Url
        }),
        'header': fields.List(fields.Nested({
            'headerName': fields.String,
            'headerValue': fields.String
        })),
        'param': fields.List(fields.Nested({
            'paramKey': fields.String,
            'paramValue': fields.String,
            'paramDesc': fields.String
        })),
        'additionalparam': fields.List(fields.Nested({
            'paramKey': fields.String,
            'paramValue': fields.String,
            'paramDesc': fields.String
        }))
    }

    resource_fields_post = {
        'envID': fields.Integer,
        'success': fields.Boolean
    }

    resource_fields_delete = {
        'envID': fields.Integer,
        'success': fields.Boolean
    }

    """
        @api {get} /api/v1/env/ 环境-详情
        @apiDescription 获取一个环境的详情
        @apiName env-detail
        @apiGroup Env

        @apiParam {Number} envID 环境ID 

        @apiSuccess {String} envName 环境名称
        @apiSuccess {String} envDesc 环境描述
        @apiSuccess {object} uri 环境uri
        @apiSuccess {String} uri.uri uri详情
        
        @apiSuccess {String} envName 环境名称
        @apiSuccess {String} envName 环境名称
        

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 OK
        {
            "success": true
        }
    """

    @marshal_with(resource_fields_get)
    def get(self):
        '''
        查询环境
        :param env_id: 环境ID
        :return:
        '''
        # 1. 入参解析器
        parser = reqparse.RequestParser()

        # 2. 新增解析字段
        parser.add_argument('env_id', type=int, location='args', help='env_id验证失败')

        # 3. 拿到env_id
        env_id = request.args.get('env_id')
        args = parser.parse_args()
        print(args)

        # 2. 查询资源是否存在
        abort_if_todo_doesnt_exist(env_id)

        # 3. 查询资源
        env = EoApiEnv.query.get(env_id)
        return env

    """
        @api {post} /api/v1/env/ 环境-新增
        @apiDescription 新增一个环境
        @apiName add-env
        @apiGroup Env
        
        @apiHeader {String} Content-Type=application/json json格式
        @apiHeaderExample {json} Header-Example:
            { "Content-Type": "application/json" }        
            
        @apiParamExample {json} Request-Example:
            {
            "env_projectID":2,
            "env_name": "测试环境",
            "env_desc": "application/x-www-form-urlencoded",
            "env_uri": {
                "env_uri": "giant.dev.yunlu6.com"
            },
            "env_header": [
                {
                    "headerName": "Accept-Encoding1",
                    "headerValue": "gzip"
                },
                {
                    "headerName": "Accept-Encoding2",
                    "headerValue": "gzip"
                },
                {
                    "headerName": "Accept-Encoding3",
                    "headerValue": "gzip"
                }
            ],
            "env_param": [
                {
                    "paramKey": "token",
                    "paramValue": "asdfjkj123kjdfjskdsadf",
                    "paramDesc": null
                }
            ],
            "env_additionalparam": [
                {
                    "paramKey": "addtional_token",
                    "paramValue": "13849sdf87a8d09fqherjhadf",
                    "paramDesc": null
                }
            ]
        }
                    
        @apiParam {Number} envID 环境ID 
        @apiParam {Number} env_projectID 项目ID
        @apiParam {String} envName 环境名称
        @apiParam {String} envDesc 环境描述
        @apiParam {object} uri 环境uri
        @apiParam {String} uri.uri uri详情
        @apiParam {String[]} env_header 请求头
        @apiParam {String} env_header.headerName 请求头名
        @apiParam {String} env_header.headerValue 请求头值
        @apiParam {String[]} env_param 全局参数
        @apiParam {String} env_param.paramKey 参数名
        @apiParam {String} env_param.paramValue 参数值
        @apiParam {String} env_param.paramDesc 参数描述
        @apiParam {String[]} env_additionalparam 额外参数
        @apiParam {String} env_additionalparam.paramKey 额外参数名
        @apiParam {String} env_additionalparam.paramValue 额外参数值
        @apiParam {String} env_additionalparam.paramDesc 额外参数描述
        

        @apiSuccess {String} envID 环境ID
        @apiSuccess {Boolean} success 成功状态

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 OK
        {
            "success": true,
            'envID':1
        }
    """

    @marshal_with(resource_fields_post)
    def post(self):
        '''
        新增一条环境
        :return:
        '''
        print('post come in')

        # 1. 入参解析器
        # parser = reqparse.RequestParser()

        # 2. 新增解析字段
        # parser.add_argument('env_projectID', type=int, location='form', help='env_projectID验证失败')

        # 1. 拿到json格式数据
        args = request.get_json()

        # 2. 解析参数
        env_projectID = args['env_projectID']  # 项目ID
        envName = args['env_name']  # 环境名称
        envDesc = args['env_desc']  # 环境描述
        envUri = args['env_uri']['env_uri']  # 环境uri

        # 环境
        env = EoApiEnv(envName=envName, envDesc=envDesc)
        # uri
        uri = EoApiEnvFrontUri(uri=envUri)
        # 一对一关系
        env.uri = uri
        env.projectID = env_projectID

        # 解析头文件
        header = args['env_header']
        for i in header:
            headerName = i['headerName']
            headerValue = i['headerValue']
            header = EoApiEnvHeader(headerName=headerName, headerValue=headerValue)
            env.header.append(header)

        # 解析参数
        param = args['env_param']
        for k in param:
            paramKey = k['paramKey']
            paramValue = k['paramValue']
            paramDesc = k['paramDesc']
            param = EoApiEnvParam(paramKey=paramKey, paramValue=paramValue, paramDesc=paramDesc)
            env.param.append(param)

        # 解析额外参数
        aparam = args['env_additionalparam']
        for j in aparam:
            aparamKey = j['paramKey']
            aparamValue = j['paramValue']
            aparamDesc = j['paramDesc']
            param = EoApiEnvAdditionalParam(paramKey=aparamKey, paramValue=aparamValue, paramDesc=aparamDesc)
            env.additionalparam.append(param)

        db.session.add(env)
        db.session.commit()

        return {
            'success': True,
            'envID': env.envID
        }

    def put(self):
        pass

    """
        @api {delete} /api/v1/env 环境-删除
        @apiDescription  删除一个环境
        @apiName delete-env
        @apiGroup Env
        
        @apiParam {Number} envID 环境ID
        
        @apiSuccess {Boolean} success 成功状态
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 OK
        {
            "success": true
        }
    """

    def delete(self):
        # 1. 验证器
        parser = reqparse.RequestParser()
        # 2. 新增字段
        parser.add_argument('env_id', type=int, location='args', help='env_id验证失败')
        # 3. 解析参数
        args = parser.parse_args()
        env_id = args['env_id']
        print(env_id)

        # 4. 查询env
        abort_if_todo_doesnt_exist(env_id)
        env = EoApiEnv.query.filter_by(envID=env_id).first()
        # 如果环境存在：
        if env:
            db.session.delete(env)
            db.session.commit()
            return {
                'success': True,
                # 'envID': env_id
            }
        else:
            return {
                'success': False,
                'error': 'envID={0}的资源不存在!s'.format(env_id)
            }


# api.add_resource(Env, '/<env_id>/', endpoint='env')
api.add_resource(Env, '/', endpoint='env')


class EnvList(Resource):
    resource_fields_get = {
        'envID': fields.Integer,
        'projectID': fields.Integer,
        'envName': fields.String,
        'envDesc': fields.String,
    }

    """
        @api {get} /api/v1/env/list/ 环境-列表
            @apiDescription 获取环境列表
            @apiName env-list
            @apiGroup Env
    
            @apiParam {Number} projectID 项目ID 
            @apiParam {Number} [page] 页面数
            @apiParam {Number} [per_page] 每页显示条数 
    
            @apiSuccess {Number} envID 环境ID
            @apiSuccess {Number} projectID 项目ID
            @apiSuccess {String} envName 环境名称
            @apiSuccess {String} envDesc 环境描述
            
    
            @apiSuccessExample {json} Success-Response:
            HTTP/1.1 201 OK
            [
                {
                    "envID": 2,
                    "projectID": 2,
                    "envName": "测试环境",
                    "envDesc": "application/x-www-form-urlencoded"
                },
                {
                    "envID": 9,
                    "projectID": 2,
                    "envName": "测试环境",
                    "envDesc": "application/x-www-form-urlencoded"
                }
            ]
    """

    @marshal_with(resource_fields_get)
    def get(self):
        # 解析
        parser = reqparse.RequestParser()

        # 字段
        parser.add_argument('project_id', type=int, location='args', help='project_id验证失败')
        parser.add_argument('page', type=int, location='args', help='page验证失败')
        parser.add_argument('per_page', type=int, location='args', help='per_page验证失败')
        args = parser.parse_args()

        # 获取
        project_id = args['project_id']
        page = args['page']
        per_page = args['per_page']

        abrot_if_todo_doesnt_exist_project(project_id)
        # 分页
        pagination = EoApiEnv.query.filter_by(projectID=project_id).order_by(EoApiEnv.envID).paginate(page=page, per_page=per_page, error_out=False)
        env = pagination.items
        return env


api.add_resource(EnvList, '/list/', endpoint='envlist')

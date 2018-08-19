# Author:Xiaojingyuan

from exts import db
from flask import Blueprint
from flask_restful import Api, Resource, fields, marshal_with, abort, reqparse
from models import EoProject
import datetime
from utils import restful

project_bp = Blueprint('project', __name__, url_prefix='/api/v1/project')
api = Api(project_bp)  # 使用蓝图注册api


# 404操作
def abort_if_todo_doesnt_exist_project(project_id):
    if EoProject.query.filter_by(projectID=project_id).first() == None:
        abort(404, message='ID={0}的资源不存在!'.format(project_id))


# 环境详情
class Project(Resource):
    resource_fields_get = {
        'projectID': fields.Integer,
        'projectType': fields.Integer,
        'projectName': fields.String,
        'projectCreateTime': fields.String,
        'projectUpdateTime': fields.String,
        'projectVersion': fields.String,
    }

    resource_fields_post = {
        'projectID': fields.Integer,
        'success': fields.Boolean
    }

    resource_fields_put = {'success': fields.Boolean}

    resource_fields_delete = {
        'projectID': fields.Integer,
        'success': fields.Boolean
    }
    """
        @api {get} /api/v1/project/ 项目-详情
        @apiDescription 获取具体项目详情
        @apiName details
        @apiGroup Project

        @apiParam {Number} project_id 项目ID

        @apiSuccess {Number} projectID 项目ID
        @apiSuccess {Number} projectType 项目类型
        @apiSuccess {String} projectCreateTime 项目创建时间
        @apiSuccess {String} projectUpdateTime 项目更新时间
        @apiSuccess {String} projectVersion 项目版本号

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "projectID": 1,
            "projectType": 1,
            "projectName": "测试项目111",
            "projectCreateTime": "2018-07-17 11:04:18",
            "projectUpdateTime": "2018-07-17 11:04:18",
            "projectVersion": "1.1"
        }
    """

    @marshal_with(resource_fields_get)
    def get(self):
        '''
        项目 - 详情
        :param : project_id 项目ID
        :return:
        '''
        # 1. 入参解析器
        parser = reqparse.RequestParser()

        # 2. 新增解析字段
        parser.add_argument(
            'project_id',
            type=int,
            location='args',
            help='project_id验证失败',
            required=True)

        # 3. 拿到project_id
        args = parser.parse_args()
        project_id = args['project_id']
        abort_if_todo_doesnt_exist_project(project_id)

        # 4. 查询资源
        project = EoProject.query.get(project_id)
        # return restful.success(data=project, message='get')
        return project

    """
        @api {post} /api/v1/project/ 项目-新增
        @apiDescription 新增一个项目
        @apiName add-project
        @apiGroup Project

        @apiParam {Number} projectType 项目类型
        @apiParam {String} projectName 项目名称
        @apiParam {String} projectVersion 项目版本号
        
        @apiSuccess {Number} projectID 项目ID
        @apiSuccess {Boolean} success 成功状态
        
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 OK
        {
            "projectID": 21,
            "success": true
        }
    """

    @marshal_with(resource_fields_post)
    def post(self):
        # 1. 入参解析器
        parser = reqparse.RequestParser()

        # 2. 新增解析字段
        parser.add_argument(
            'projectType',
            type=int,
            location=['form', 'json'],
            help='projectType验证失败',
            required=True)
        parser.add_argument(
            'projectName',
            type=str,
            location=['form', 'json'],
            help='projectName验证失败',
            required=True)
        parser.add_argument(
            'projectVersion',
            type=str,
            location=['form', 'json'],
            help='projectVersion验证失败',
            required=True)

        # 3. 解析
        args = parser.parse_args()
        projectType = args['projectType']
        projectName = args['projectName']
        projectVersion = args['projectVersion']

        # 4. 提交数据
        project = EoProject(
            projectType=projectType,
            projectName=projectName,
            projectVersion=projectVersion)
        db.session.add(project)
        db.session.commit()

        return {'success': True, 'projectID': project.projectID}, 201

    """
        @api {put} /api/v1/project/ 项目-更新
        @apiDescription 更新项目详情
        @apiName update-project
        @apiGroup Project
        
        @apiParam {Number} projectID 项目ID
        @apiParam {Number} [projectType] 项目类型
        @apiParam {String} [projectName] 项目名称
        @apiParam {String} [projectVersion] 项目版本号
        
        @apiSuccess {Boolean} success 成功状态
        
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 204 OK
        {
            "projectID": 21,
            "success": true
        }
    """

    @marshal_with(resource_fields_put)
    def put(self):
        # 1. 入参解析器
        parser = reqparse.RequestParser()

        # 2. 新增解析字段
        parser.add_argument(
            'projectID',
            type=int,
            location='form',
            help='projectID验证失败',
            required=True)
        parser.add_argument(
            'projectType', type=int, location='form', help='projectType验证失败')
        parser.add_argument(
            'projectName', type=str, location='form', help='projectName验证失败')
        parser.add_argument(
            'projectVersion',
            type=str,
            location='form',
            help='projectVersion验证失败')

        # 3. 解析
        args = parser.parse_args()
        projectID = args['projectID']
        abort_if_todo_doesnt_exist_project(projectID)
        projectName = args['projectName']
        projectVersion = args['projectVersion']
        projectType = args['projectType']

        # 4. 更新
        project = EoProject.query.filter_by(projectID=projectID).first()
        if projectName != None:
            project.projectName = projectName
        if projectType != None:
            project.projectType = projectType
        if projectVersion != None:
            project.projectVersion = projectVersion
        project.projectUpdateTime = datetime.datetime.now()

        db.session.commit()
        return {'success': True}, 204

    """
        @api {delete} /api/v1/project/ 项目-删除
        @apiDescription 删除一个项目
        @apiName delete-project
        @apiGroup Project

        @apiParam {Number} projectID 项目ID 

        @apiSuccess {Boolean} success 成功状态

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 OK
        {
            "success": true
        }
    """

    def delete(self):
        parser = reqparse.RequestParser()

        # 2. 新增解析字段
        parser.add_argument(
            'projectID',
            type=int,
            location='form',
            help='projectID验证失败',
            required=True)

        # 3. 解析
        args = parser.parse_args()
        projectID = args['projectID']
        abort_if_todo_doesnt_exist_project(projectID)
        project = EoProject.query.get(projectID)
        db.session.delete(project)
        db.session.commit()
        return {'success': True}, 200


api.add_resource(Project, '/', endpoint='project')


class ProjectList(Resource):
    resource_fields_get = {
        'meta':
        fields.Nested({
            'page_size': fields.Integer,
            'total': fields.Integer
        }),
        'projects':
        fields.List(
            fields.Nested({
                'projectID': fields.Integer,
                'projectType': fields.Integer,
                'projectName': fields.String,
                'projectCreateTime': fields.String,
                'projectUpdateTime': fields.String,
                'projectVersion': fields.String
            }))
    }
    """
    @api {get} /api/v1/project/list/ 项目-列表
    @apiDescription 获取项目列表
    @apiName project-list
    @apiGroup Project

    @apiParam {Number} [page] 页数
    @apiParam {Number} [per_page] 每页数

    @apiSuccess {Number} projectID 项目ID
    @apiSuccess {Number} projectType 项目类型
    @apiSuccess {String} projectCreateTime 项目创建时间
    @apiSuccess {String} projectUpdateTime 项目更新时间
    @apiSuccess {String} projectVersion 项目版本号
    
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
    "meta": {
        "page_size": 10,
        "total": 1
    },
    "projects": [
        {
            "projectID": 1,
            "projectType": 1,
            "projectName": "测试项目111",
            "projectCreateTime": "2018-07-17 11:04:18",
            "projectUpdateTime": "2018-07-17 11:04:18",
            "projectVersion": "1.1"
        },
        {
            "projectID": 2,
            "projectType": 1,
            "projectName": "测试项目111",
            "projectCreateTime": "2018-07-17 11:05:06",
            "projectUpdateTime": "2018-07-17 11:05:06",
            "projectVersion": "1.1"
        }
    ]
}
    """

    @marshal_with(resource_fields_get)
    def get(self):
        '''
        项目 - 列表
        :return:
        '''
        # 解析
        parser = reqparse.RequestParser()

        # 字段
        parser.add_argument('page', type=int, location='args', help='page验证失败')
        parser.add_argument(
            'per_page', type=int, location='args', help='per_page验证失败')
        args = parser.parse_args()

        # 获取
        page = args['page']
        per_page = args['per_page']

        # 条数
        count = db.session.query(db.func.count(
            EoProject.projectID)).first()  # 元祖('19',)
        count = list(count)[0]

        # 分页
        pagination = EoProject.query.order_by(EoProject.projectID).paginate(
            page=page, per_page=per_page, error_out=False)
        project = pagination.items

        return {'projects': project, 'meta': {'total': count, 'page_size': 10}}


api.add_resource(ProjectList, '/list/', endpoint='projectlist')

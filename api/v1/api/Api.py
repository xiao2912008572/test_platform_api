# Author:Xiaojingyuan

from exts import db
from flask import Blueprint, session, url_for, render_template, views, request, jsonify
from flask_restful import Api, Resource, fields, marshal_with, abort, reqparse, inputs
from models import EoProject, EoApiGroup

api_group_bp = Blueprint('apigroup', __name__, url_prefix='/api/v1/api_group')
api = Api(api_group_bp)  # 使用蓝图注册api


# 404 - 验证api文档分组是否存在
def abort_if_todo_doesnt_exist_api_group(groupID):
    if EoApiGroup.query.filter_by(groupID=groupID).first() == None:
        abort(404, message='groupID={0}的资源不存在!'.format(groupID))


# 404 - 验证project是否存在
def abort_if_todo_doesnt_exist_project(projectID):
    if EoProject.query.filter_by(projectID=projectID).first() == None:
        abort(404, message='projectID={0}的资源不存在!'.format(projectID))


# api接口文档分组
class ApiGroup(Resource):
    # 1. 入参解析器
    parser = reqparse.RequestParser()

    resource_fields_get = {
        'groupID': fields.Integer,
        'groupName': fields.String,
        'parentGroupID': fields.Integer,
        'isChild': fields.Boolean,
    }

    resource_fields_post = {
        'success': fields.Boolean,
        'groupID': fields.Integer
    }
    resource_fields_put = {
        'success': fields.Boolean,
    }
    resource_fields_delete = {
        'success': fields.Boolean,
    }
    """
        @api {get} /api/v1/api_group/ api文档分组-详情
            @apiDescription 获取api文档分组详情
            @apiName api-group-detail
            @apiGroup Api

            @apiParam {Number} groupID api文档分组ID 

            @apiSuccess {Number} groupID api文档分组ID
            @apiSuccess {String} groupName 分组名称
            @apiSuccess {Number} parentGroupID 分组父ID
            @apiSuccess {String} isChild 是否有子分组

            @apiSuccessExample {json} Success-Response:
            HTTP/1.1 201 OK
            {
                "groupID": 3,
                "groupName": "1级分组",
                "parentGroupID": 0,
                "isChild": false
            }
    """

    @marshal_with(resource_fields_get)
    def get(self):
        '''
        获取api文档分组
        :param groupID : 分组ID
        :return:
        '''
        # 1. 新增解析字段
        self.parser.add_argument('groupID', type=int, location='args', required=True, help='groupID验证失败')

        # 2. 解析
        args = self.parser.parse_args()
        groupID = args['groupID']
        abort_if_todo_doesnt_exist_api_group(groupID)

        # 3. 查询数据
        status_group = EoApiGroup.query.get(groupID)

        # 4. 判断
        # if status_group.parentGroupID != 0:
        #     print(status_group.parentGroupID, 'parentGroupID')
        #     status_group_parent = EoProjectStatusCodeGroup.query.get(status_group.parentGroupID)
        return status_group

    """
        @api {post} /api/v1/api_group/ api文档分组-新增
            @apiDescription 新增一个api文档分组
            @apiName add-api-group
            @apiGroup Api

            @apiParam {String} groupName api文档分组名称
            @apiParam {Number} [parentGroupID] api文档分组父ID
            @apiParam {Boolean} [isChild] api文档分组是否有子分组
            @apiParam {Number} projectID 项目ID 

            @apiSuccess {String} groupID api文档分组ID
            @apiSuccess {Boolean} success 成功状态

            @apiSuccessExample {json} Success-Response:
            HTTP/1.1 201 OK
            {
                "success": true
                "groupID": 1
            }
    """

    @marshal_with(resource_fields_post)
    def post(self):
        '''
        新增api文档分组
        :return:
        '''
        # 1. 新增
        self.parser.add_argument('groupName', type=str, location='form', required=True, help='groupName校验失败')
        self.parser.add_argument('parentGroupID', type=int, location='form', help='parentGroupID校验失败')
        self.parser.add_argument('isChild', type=bool, location='form', help='isChild校验失败')
        self.parser.add_argument('projectID', type=int, location='form', required=True, help='projectID校验失败')
        args = self.parser.parse_args()

        # 2. 获取
        projectID = args['projectID']
        groupName = args['groupName']
        parentGroupID = args['parentGroupID']
        isChild = args['isChild']

        # 验证parentGroupID是否存在
        abort_if_todo_doesnt_exist_api_group(parentGroupID)

        # 验证projectID是否存在
        abort_if_todo_doesnt_exist_project(projectID)

        # 新增一条数据
        statusGroup = EoApiGroup(
            groupName=groupName,
            parentGroupID=parentGroupID,
            isChild=isChild,
            projectID=projectID
        )
        db.session.add(statusGroup)
        db.session.commit()
        return {
            'success': True,
            'groupID': statusGroup.groupID
        }

    """
        @api {put} /api/v1/api_group/ api文档分组-更新
        @apiDescription 更新一个api文档分组
        @apiName update-api-group
        @apiGroup Api

        @apiParam {Number} groupID api文档分组ID
        @apiParam {String} [groupName] api文档分组名称
        @apiParam {Number} [parentGroupID] api文档分组父ID
        @apiParam {Boolean} [isChild] api文档分组是否有子分组

        @apiSuccess {Boolean} success 成功状态

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 OK
        {
            "success": true
        }
    """

    @marshal_with(resource_fields_put)
    def put(self):
        '''
        更新api文档分组详情
        :return:
        '''
        self.parser.add_argument('groupID', type=str, location='form', required=True, help='groupID校验失败')
        self.parser.add_argument('groupName', type=str, location='form', help='groupName校验失败')
        self.parser.add_argument('parentGroupID', type=int, location='form', help='parentGroupID校验失败')
        self.parser.add_argument('isChild', type=bool, location='form', help='isChild校验失败')
        args = self.parser.parse_args()

        # 获取
        groupID = args['groupID']
        groupName = args['groupName']
        parentGroupID = args['parentGroupID']
        isChild = args['isChild']

        abort_if_todo_doesnt_exist_api_group(groupID)

        # 更新
        status_group = EoApiGroup.query.filter_by(groupID=groupID).first()
        if groupName != None:
            status_group.groupName = groupName
        if parentGroupID != None:
            abort_if_todo_doesnt_exist_api_group(parentGroupID)
            status_group.parentGroupID = parentGroupID
        if isChild != None:
            status_group.isChild = isChild

        db.session.commit()
        return {
                   'success': True
               }, 204

    """
        @api {delete} /api/v1/api_group/ api文档分组-删除
        @apiDescription 删除一个api文档分组
        @apiName delete-api-group
        @apiGroup Api

        @apiParam {Number} groupID api文档分组ID

        @apiSuccess {Boolean} success 成功状态

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 OK
        {
            "success": true
        }
    """

    @marshal_with(resource_fields_delete)
    def delete(self):
        '''
        :return:
        '''
        # 1. 新增
        self.parser.add_argument('groupID', type=int, location='form', help='groupID校验失败！')
        args = self.parser.parse_args()

        # 2. 获取
        groupID = args['groupID']

        # 验证groupID是否存在
        abort_if_todo_doesnt_exist_api_group(groupID)

        # 查询
        status_group = EoApiGroup.query.get(groupID)

        # 3. 删除数据
        db.session.delete(status_group)
        db.session.commit()

        return {
            'success': True
        }


api.add_resource(ApiGroup, '/', endpoint='apigroup')


# class Api(Resource):
#     # 1. 入参解析器
#     parser = reqparse.RequestParser()
#
#     resource_fields_get = {
#         'type': 'api',
#         'statusCode': "000000",
#         'apiInfo': fields.Nested({
#             'baseInfo': fields.Nested({
#                 'apiName': fields.String,
#                 'apiURI': fields.String,
#                 'apiProtocol': fields.Boolean,
#                 "apiSuccessMock": fields.String,
#                 "apiFailureMock": fields.String,
#                 "apiRequestType": fields.Boolean,
#                 "apiStatus": fields.Boolean,
#                 "starred": fields.Boolean,
#                 "apiRequestParamType": fields.Boolean,
#                 "apiRequestRaw": db.String,
#                 "apiFailureStatusCode": fields.String,
#                 "apiSuccessStatusCode": fields.String,
#                 "apiUpdateTime": fields.datetime,
#                 "removed": fields.Boolean,
#                 "groupID": fields.Integer,
#                 "parentGroupID": fields.Integer,
#                 "apiID": fields.Integer,
#                 "topParentGroupID": fields.Integer,
#                 "updateUserName": fields.String,
#                 "createUserName": fields.String
#             }),
#             'headerInfo': fields.List(fields.Nested({
#                 "headerName": fields.String,
#                 "headerValue": fields.String
#             })
#             ),
#             'requestInfo': fields.List(fields.Nested({
#                 "paramID": fields.Integer,
#                 "paramNotNull": fields.Boolean,
#                 "paramType": fields.Boolean,
#                 "paramName": fields.String,
#                 "paramKey": fields.String,
#                 "paramValue": fields.String,
#                 "paramLimit": fields.String,
#                 # "paramValueList": fields.String,
#             })
#             ),
#             'resultInfo': fields.List(fields.Nested({
#                 "paramID"
#                 "paramNotNull": fields.Boolean,
#                 "paramName": fields.String,
#                 "paramKey": fields.String,
#                 "paramType": fields.Boolean,
#                 # "paramValueList": fields.List(fields.Nested({
#                 #     "valueID": fields.Integer,
#                 #     "value": fields.String,
#                 #     "valueDescription": fields.String
#                 # })),
#                 "paramID": fields.Integer,
#             })
#             ),
#             'urlParam': fields.List({
#
#             }),
#             'restfulParam': fields.List({
#
#             }),
#         }),
#
#         'groupID': fields.Integer,
#         'groupName': fields.String,
#         'parentGroupID': fields.Integer,
#         'isChild': fields.Boolean,
#     }
#
#     resource_fields_post = {
#         'success': fields.Boolean,
#         'groupID': fields.Integer
#     }
#     resource_fields_put = {
#         'success': fields.Boolean,
#     }
#     resource_fields_delete = {
#         'success': fields.Boolean,
#     }
#
#     def get(self):
#         pass
#
#     def post(self):
#         pass
#
#     def put(self):
#         pass
#
#     def delete(self):
#         pass


# api.add_resource(Api, '/api/', endpoint='api')

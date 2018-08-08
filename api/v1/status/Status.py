# Author:Xiaojingyuan

from exts import db
from flask import Blueprint, session, url_for, render_template, views, request, jsonify
from flask_restful import Api, Resource, fields, marshal_with, abort, reqparse, inputs
from models import EoProject, EoProjectStatusCode, EoProjectStatusCodeGroup

status_bp = Blueprint('status', __name__, url_prefix='/api/v1/status')
api = Api(status_bp)  # 使用蓝图注册api


# 404 - 验证状态码是否存在
def abort_if_todo_doesnt_exist_status(codeID):
    if EoProjectStatusCode.query.filter_by(codeID=codeID).first() == None:
        abort(404, message='codeID={0}的资源不存在!'.format(codeID))


# 404 - 验证状态码分组是否存在
def abort_if_todo_doesnt_exist_statusList(groupID):
    if EoProjectStatusCodeGroup.query.filter_by(groupID=groupID).first() == None:
        abort(404, message='groupID={0}的资源不存在!'.format(groupID))


# 404 - 验证project是否存在
def abort_if_todo_doesnt_exist_project(projectID):
    if EoProject.query.filter_by(projectID=projectID).first() == None:
        abort(404, message='projectID={0}的资源不存在!'.format(projectID))


class Status(Resource):
    # 1. 入参解析器
    parser = reqparse.RequestParser()

    resource_fields_get = {
        'code': fields.String,
        'codeDescription': fields.String,
        'groupID': fields.Integer
    }
    resource_fields_post = {
        'success': fields.Boolean,
        'codeID': fields.Integer
    }
    resource_fields_put = {
        'success': fields.Boolean
    }
    resource_fields_delete = {
        'success': fields.Boolean
    }

    """
        @api {get} /api/v1/status/ 状态码-详情
        @apiDescription 获取项目的状态码
        @apiName status-code
        @apiGroup Status

        @apiParam {Number} codeID 状态码ID

        @apiSuccess {String} code 状态码
        @apiSuccess {String} codeDescription 状态码描述
        @apiSuccess {Number} groupID 分组ID

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "code": "200",
            "codeDescription": "成功",
            "groupID": 1
        }
    """

    @marshal_with(resource_fields_get)
    def get(self):
        '''
        状态码详情
        :return:
        '''
        # 2. 新增解析字段
        self.parser.add_argument('codeID', type=int, location='args', help='codeID验证失败', required=True)

        # 3. 拿到codeID
        args = self.parser.parse_args()
        codeID = args['codeID']
        abort_if_todo_doesnt_exist_status(codeID)

        # 查询资源
        status = EoProjectStatusCode.query.get(codeID)
        return status

    """
        @api {post} /api/v1/status/ 状态码-新增
        @apiDescription 新增一个状态码
        @apiName add-status
        @apiGroup Status

        @apiParam {String} code 状态码
        @apiParam {String} codeDescription 状态码描述
        @apiParam {Number} [groupID] 分组ID

        @apiSuccess {Number} codeID 状态码ID
        @apiSuccess {Boolean} success 成功状态

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
           "success": true,
            "codeID": 7
        }
    """

    @marshal_with(resource_fields_post)
    def post(self):
        '''
        新增状态码
        :return:
        '''
        # 1. 新增字段
        self.parser.add_argument('code', type=str, location='form', required=True, help='code校验失败')
        self.parser.add_argument('codeDescription', type=str, location='form', required=True, help='codeDescription校验失败')
        self.parser.add_argument('groupID', type=int, location='form', help='groupID校验失败')

        # 2. 解析
        args = self.parser.parse_args()
        code = args['code']
        codeDescription = args['codeDescription']
        groupID = args['groupID']

        # 3. 提交数据
        status = EoProjectStatusCode(code=code, codeDescription=codeDescription)
        status.groupID = groupID
        db.session.add(status)
        db.session.commit()

        return {
            'success': True,
            'codeID': status.codeID
        }

    """
        @api {put} /api/v1/status/ 状态码-更新
        @apiDescription 更新状态码
        @apiName update-status
        @apiGroup Status

        @apiParam {Number} codeID 状态码ID
        @apiParam {String} [code] 状态码
        @apiParam {String} [codeDescription] 状态码描述
        @apiParam {Number} [groupID] 分组ID

        @apiSuccess {Number} codeID 状态码ID
        @apiSuccess {Boolean} success 成功状态

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
           "success": true,
        }
        """

    @marshal_with(resource_fields_put)
    def put(self):
        self.parser.add_argument('codeID', type=int, location='form', required=True, help='codeID校验失败')
        self.parser.add_argument('code', type=str, location='form', help='code校验失败')
        self.parser.add_argument('codeDescription', type=str, location='form', help='codeDescription校验失败')
        self.parser.add_argument('groupID', type=int, location='form', help='groupID校验失败')

        # 2. 解析
        args = self.parser.parse_args()
        codeID = args['codeID']
        abort_if_todo_doesnt_exist_status(codeID=codeID)  # 验证codeID是否存在
        code = args['code']
        codeDescription = args['codeDescription']
        groupID = args['groupID']

        # 3. 更新
        status = EoProjectStatusCode.query.get(codeID)
        if code != None:
            status.code = code
        if codeDescription != None:
            status.codeDescription = codeDescription
        if groupID != None:
            status.groupID = groupID

        db.session.commit()
        return {
                   'success': True,
               }, 204

    """
        @api {delete} /api/v1/status/ 状态码-删除
        @apiDescription 删除状态码
        @apiName delete-status
        @apiGroup Status

        @apiParam {Number} codeID 状态码ID

        @apiSuccess {Boolean} success 成功状态

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
           "success": true,
        }
    """

    @marshal_with(resource_fields_put)
    def delete(self):
        '''
        删除一个状态码
        :return:
        '''
        self.parser.add_argument('codeID', type=int, location='form', required=True, help='codeID校验失败')
        args = self.parser.parse_args()
        codeID = args['codeID']
        abort_if_todo_doesnt_exist_status(codeID=codeID)
        status = EoProjectStatusCode.query.filter_by(codeID=codeID).first()
        db.session.delete(status)
        db.session.commit()
        return {
            'success': True
        }


api.add_resource(Status, '/', endpoint='status')


class StatusGroup(Resource):
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
        @api {get} /api/v1/status/list/ 状态码分组-详情
            @apiDescription 获取状态码分组详情
            @apiName status-group-detail
            @apiGroup Status

            @apiParam {Number} groupID 状态码分组ID 

            @apiSuccess {Number} groupID 状态码分组ID
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
        获取状态码分组
        :param groupID : 分组ID
        :return:
        '''
        # 1. 新增解析字段
        self.parser.add_argument('groupID', type=int, location='args', required=True, help='groupID验证失败')

        # 2. 解析
        args = self.parser.parse_args()
        groupID = args['groupID']
        abort_if_todo_doesnt_exist_statusList(groupID)

        # 3. 查询数据
        status_group = EoProjectStatusCodeGroup.query.get(groupID)

        # 4. 判断
        # if status_group.parentGroupID != 0:
        #     print(status_group.parentGroupID, 'parentGroupID')
        #     status_group_parent = EoProjectStatusCodeGroup.query.get(status_group.parentGroupID)
        return status_group

    """
        @api {post} /api/v1/status/group/ 状态码分组-新增
            @apiDescription 新增一个状态码分组
            @apiName add-status-group
            @apiGroup Status
            
            @apiParam {String} groupName 状态码分组名称
            @apiParam {Number} [parentGroupID] 状态码分组父ID
            @apiParam {Boolean} [isChild] 状态码分组是否有子分组
            @apiParam {Number} projectID 项目ID 
    
            @apiSuccess {String} groupID 状态码分组ID
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
        新增状态码分组
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
        abort_if_todo_doesnt_exist_statusList(parentGroupID)

        # 验证projectID是否存在
        abort_if_todo_doesnt_exist_project(projectID)

        # 新增一条数据
        statusGroup = EoProjectStatusCodeGroup(
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
        @api {put} /api/v1/status/group/ 状态码分组-更新
        @apiDescription 更新一个状态码分组
        @apiName update-status-group
        @apiGroup Status

        @apiParam {Number} groupID 状态码分组ID
        @apiParam {String} [groupName] 状态码分组名称
        @apiParam {Number} [parentGroupID] 状态码分组父ID
        @apiParam {Boolean} [isChild] 状态码分组是否有子分组

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
        更新状态码分组详情
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

        abort_if_todo_doesnt_exist_statusList(groupID)

        # 更新
        status_group = EoProjectStatusCodeGroup.query.filter_by(groupID=groupID).first()
        if groupName != None:
            status_group.groupName = groupName
        if parentGroupID != None:
            abort_if_todo_doesnt_exist_statusList(parentGroupID)
            status_group.parentGroupID = parentGroupID
        if isChild != None:
            status_group.isChild = isChild

        db.session.commit()
        return {
                   'success': True
               }, 204

    """
        @api {delete} /api/v1/status/group/ 状态码分组-删除
        @apiDescription 删除一个状态码分组
        @apiName delete-status-group
        @apiGroup Status

        @apiParam {Number} groupID 状态码分组ID

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
        abort_if_todo_doesnt_exist_statusList(groupID)

        # 查询
        status_group = EoProjectStatusCodeGroup.query.get(groupID)

        # 3. 删除数据
        db.session.delete(status_group)
        db.session.commit()

        return {
            'success': True
        }


api.add_resource(StatusGroup, '/group/', endpoint='statusgroup')

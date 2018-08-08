# # Author:Xiaojingyuan
from exts import db
from datetime import datetime


# CREATE TABLE `eo_project` (
#   `projectID` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `projectType` tinyint(1) unsigned NOT NULL,
#   `projectName` varchar(255) COLLATE utf8_bin NOT NULL,
#   `projectUpdateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `projectVersion` varchar(6) COLLATE utf8_bin NOT NULL DEFAULT '1.0',
#   PRIMARY KEY (`projectID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin

# 🌟 4. 项目表:用于存储项目的相关信息
class EoProject(db.Model):
    __tablename__ = 'eo_project'

    # 项目ID
    projectID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 项目类型
    projectType = db.Column(db.Integer, nullable=False)
    # 项目名
    projectName = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    # 项目创建时间
    projectCreateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # 项目更新时间
    projectUpdateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # 项目版本
    projectVersion = db.Column(db.String(6, 'utf8_bin'), nullable=False)


# CREATE TABLE `eo_api_env` (
#   `envID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `envName` varchar(255) NOT NULL,
#   `projectID` int(10) unsigned NOT NULL,
#   PRIMARY KEY (`envID`,`projectID`)
# ) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8

# 🌟 5. 环境管理 - 环境表1 - eo_api_env
'''
关系图：
4.项目表 和 5.环境表 : 一对多关系 
'''


class EoApiEnv(db.Model):
    __tablename__ = 'eo_api_env'

    # 环境ID
    envID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 环境名称
    envName = db.Column(db.String(255), nullable=False)
    # 环境说明
    envDesc = db.Column(db.String(255), nullable=True)
    # 项目ID - 外键
    projectID = db.Column(db.Integer, db.ForeignKey("eo_project.projectID"))

    # 一对多关系映射
    project = db.relationship("EoProject", backref='apienv')

    def __repr__(self):
        return "<Article(envName:%s)>" % self.envName


# CREATE TABLE `eo_api_env_front_uri` (
#   `envID` int(10) unsigned NOT NULL,
#   `uri` varchar(255) NOT NULL,
#   `uriID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `applyProtocol` varchar(4) NOT NULL DEFAULT '-1',
#   PRIMARY KEY (`uriID`,`envID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8

# 🌟 6. 环境管理 - 环境表2 - eo_api_env_front_uri
'''
关系图：
5.项目表 和 6.环境uri表 : 一对一关系
'''


class EoApiEnvFrontUri(db.Model):
    __tablename__ = 'eo_api_env_front_uri'

    # uriID
    uriID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 前置uri
    uri = db.Column(db.String(255), nullable=False)
    # 鉴权信息
    applyProtocol = db.Column(db.String(4), nullable=True)

    # 外键 - envID
    envID = db.Column(db.Integer, db.ForeignKey("eo_api_env.envID"))
    # 一对一关系映射
    env = db.relationship("EoApiEnv", backref=db.backref('uri', uselist=False))


# CREATE TABLE `eo_api_env_header` (
#   `headerID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `envID` int(11) NOT NULL,
#   `applyProtocol` varchar(255) DEFAULT NULL,
#   `headerName` varchar(255) NOT NULL,
#   `headerValue` text NOT NULL,
#   PRIMARY KEY (`headerID`,`envID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8

# 🌟 7. 环境管理 - 请求头表 - eo_api_env_front_uri
'''
关系图：
5.项目表 和 7.请求头表 : 一对多关系 
'''


class EoApiEnvHeader(db.Model):
    __tablename__ = 'eo_api_env_header'

    # headerID
    headerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 请求头名称
    headerName = db.Column(db.String(255), nullable=False)
    # 请求头值
    headerValue = db.Column(db.String(255), nullable=False)

    # envID
    envID = db.Column(db.Integer, db.ForeignKey("eo_api_env.envID"))

    # 一对多关系映射
    env = db.relationship("EoApiEnv", backref="header")


# CREATE TABLE `eo_api_env_param` (
#   `paramID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `envID` int(10) unsigned NOT NULL,
#   `paramKey` varchar(255) NOT NULL,
#   `paramValue` text NOT NULL,
#   PRIMARY KEY (`paramID`,`envID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8

# 🌟 8. 环境管理 - 全局参数表 - eo_api_env_param
'''
关系图：
5.项目表 和 8.全局参数 : 一对多关系 
'''


class EoApiEnvParam(db.Model):
    __tablename__ = 'eo_api_env_param'

    # paramID
    paramID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 参数键
    paramKey = db.Column(db.String(255), nullable=False)
    # 参数值
    paramValue = db.Column(db.String(255), nullable=False)
    # 参数描述
    paramDesc = db.Column(db.String(255), nullable=True)

    # envID
    envID = db.Column(db.Integer, db.ForeignKey("eo_api_env.envID"))

    # 一对多关系映射
    env = db.relationship("EoApiEnv", backref="param")


# CREATE TABLE `eo_api_env_param_additional` (
#   `paramID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `envID` int(10) unsigned NOT NULL,
#   `paramKey` varchar(255) NOT NULL,
#   `paramValue` text NOT NULL,
#   PRIMARY KEY (`paramID`,`envID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8

# 🌟 9. 环境管理 - 额外参数表 - eo_api_env_param_additional
'''
关系图：
5.项目表 和 8.全局参数 : 一对多关系 
'''


class EoApiEnvAdditionalParam(db.Model):
    __tablename__ = 'eo_api_env_param_additional'

    # paramID
    paramID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 参数键
    paramKey = db.Column(db.String(255), nullable=False)
    # 参数值
    paramValue = db.Column(db.String(255), nullable=False)
    # 参数描述
    paramDesc = db.Column(db.String(255), nullable=True)

    # envID
    envID = db.Column(db.Integer, db.ForeignKey("eo_api_env.envID"))

    # 一对多关系映射
    env = db.relationship("EoApiEnv", backref="additionalparam")


# CREATE TABLE `eo_project_status_code` (
#   `codeID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `code` varchar(255) NOT NULL,
#   `codeDescription` varchar(255) NOT NULL,
#   `groupID` int(10) unsigned NOT NULL,
#   PRIMARY KEY (`codeID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8

# 🌟 10. 状态码管理
'''
状态码分组 和 状态码 : 一对多关系
'''


class EoProjectStatusCode(db.Model):
    __tablename__ = 'eo_project_status_code'

    codeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(255), nullable=False)
    codeDescription = db.Column(db.String(255), nullable=False)

    # 外键
    groupID = db.Column(db.Integer, db.ForeignKey("eo_project_status_code_group.groupID"))

    # 关系
    status_code_group = db.relationship("EoProjectStatusCodeGroup", backref="status_code")


# CREATE TABLE `eo_project_status_code_group` (
#   `groupID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `projectID` int(10) unsigned NOT NULL,
#   `groupName` varchar(255) NOT NULL,
#   `parentGroupID` int(10) unsigned NOT NULL DEFAULT '0',
#   `isChild` tinyint(3) unsigned NOT NULL DEFAULT '0',
#   PRIMARY KEY (`groupID`,`projectID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8

# 🌟 11. 状态码分组管理
'''
项目表 和 状态码分组 : 一对多关系
'''


class EoProjectStatusCodeGroup(db.Model):
    __tablename__ = 'eo_project_status_code_group'

    groupID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupName = db.Column(db.String(255), nullable=False)
    parentGroupID = db.Column(db.Integer, nullable=False, default=0)
    isChild = db.Column(db.Boolean, nullable=False, default=False)

    # 外键
    projectID = db.Column(db.Integer, db.ForeignKey("eo_project.projectID"))

    # 关系
    project = db.relationship("EoProject", backref="status_code_group")


# CREATE TABLE `eo_api_group` (
#   `groupID` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `groupName` varchar(30) COLLATE utf8_bin NOT NULL,
#   `projectID` int(11) unsigned NOT NULL,
#   `parentGroupID` int(10) unsigned NOT NULL DEFAULT '0',
#   `isChild` tinyint(3) unsigned NOT NULL DEFAULT '0',
#   PRIMARY KEY (`groupID`,`projectID`),
#   KEY `groupID` (`groupID`),
#   KEY `projectID` (`projectID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin

# 🌟 12. 接口文档 - 接口分组表
'''
项目表 和 接口分组 : 一对多关系
'''


class EoApiGroup(db.Model):
    __tablename__ = 'eo_api_group'

    groupID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupName = db.Column(db.String(255), nullable=False)
    parentGroupID = db.Column(db.Integer, nullable=False, default=0)
    isChild = db.Column(db.Boolean, nullable=False, default=False)

    # 外键
    projectID = db.Column(db.Integer, db.ForeignKey("eo_project.projectID"))

    # 关系
    project = db.relationship("EoProject", backref="api_group")


# CREATE TABLE `eo_api` (
#   `apiID` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `apiName` varchar(255) COLLATE utf8_bin NOT NULL,
#   `apiURI` varchar(255) COLLATE utf8_bin NOT NULL,
#   `apiProtocol` tinyint(1) unsigned NOT NULL,
#   `apiFailureMock` text COLLATE utf8_bin,
#   `apiSuccessMock` text COLLATE utf8_bin,
#   `apiRequestType` tinyint(1) unsigned NOT NULL,
#   `apiSuccessMockType` tinyint(1) unsigned NOT NULL DEFAULT '0',
#   `apiFailureMockType` tinyint(1) unsigned NOT NULL DEFAULT '0',
#   `apiStatus` tinyint(1) unsigned NOT NULL DEFAULT '0',
#   `apiUpdateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   `groupID` int(11) unsigned NOT NULL,
#   `projectID` int(11) unsigned NOT NULL,
#   `starred` tinyint(1) unsigned NOT NULL DEFAULT '0',
#   `removed` tinyint(1) unsigned NOT NULL DEFAULT '0',
#   `removeTime` timestamp NULL DEFAULT NULL,
#   `apiNoteType` tinyint(1) unsigned NOT NULL DEFAULT '0',
#   `apiNoteRaw` text COLLATE utf8_bin,
#   `apiNote` text COLLATE utf8_bin,
#   `apiRequestParamType` tinyint(3) unsigned NOT NULL DEFAULT '0',
#   `apiRequestRaw` text COLLATE utf8_bin,
#   `updateUserID` int(11) NOT NULL DEFAULT '0',
#   `mockRule` text COLLATE utf8_bin,
#   `mockResult` text COLLATE utf8_bin,
#   `mockConfig` text COLLATE utf8_bin,
#   `apiSuccessStatusCode` varchar(255) COLLATE utf8_bin DEFAULT '200',
#   `apiFailureStatusCode` varchar(255) COLLATE utf8_bin DEFAULT '200',
#   `beforeInject` longtext COLLATE utf8_bin,
#   `afterInject` longtext COLLATE utf8_bin,
#   PRIMARY KEY (`apiID`,`groupID`,`apiURI`),
#   KEY `groupID` (`groupID`),
#   KEY `apiID` (`apiID`),
#   KEY `projectID` (`projectID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin

# 🌟 13. 接口文档 - 接口表
'''
接口分组表 和 接口表 : 一对多关系
'''


# TODO 未加入mock相关字段 mockRule mockResult mockConfig
# TODO 未加入代码注入功能 beforeInject afterInject

class EoApi(db.Model):
    __tablename__ = 'eo_api'

    apiID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    apiName = db.Column(db.String(100), nullable=False)  # 接口名称
    apiURI = db.Column(db.String(100), nullable=False)  # 接口URI
    apiProtocol = db.Column(db.Boolean, nullable=False)  # 接口协议
    apiFailureMock = db.Column(db.Text)  # 失败的示例
    apiSuccessMock = db.Column(db.Text)  # 成功的示例
    apiRequestType = db.Column(db.Boolean, nullable=False)  # 接口请求类型
    # apiSuccessMockType = db.Column(db.Boolean, nullable=False, default=0) # 成功Mock类型
    # apiFailureMockType = db.Column(db.Boolean, nullable=False, default=0) # 失败Mock类型
    apiStatus = db.Column(db.Boolean, nullable=False, default=0)  # api状态
    apiUpdateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 接口更新时间
    starred = db.Column(db.Boolean, nullable=False, default=0)  #
    removed = db.Column(db.Boolean, nullable=False, default=0)  # 移除
    removeTime = db.Column(db.DateTime, nullable=True, default=None)  # 移除时间
    # apiNoteType = db.Column(db.Boolean, nullable=False, default=0) # 详细说明类型
    # apiNoteRaw = db.Column(db.Text) # 详细说明
    apiRequestParamType = db.Column(db.Boolean(3), nullable=False, default=0)  # 请求参数类型
    apiRequestRaw = db.Column(db.Text)  # 请求参数
    updateUserId = db.Column(db.Integer, nullable=False, default=0)  # 更新用户
    apiSuccessStatusCode = db.Column(db.String(255), nullable=True, default=200)  # 成功状态码
    apiFailureStatusCode = db.Column(db.String(255), nullable=True, default=200)  # 失败状态码

    # 外键1 - 分组ID
    groupID = db.Column(db.Integer, db.ForeignKey("eo_api_group.groupID"))  # 分组ID
    # 关系1
    group = db.relationship("EoApiGroup", backref="apis")

    # 外键2 - 项目ID
    projectID = db.Column(db.Integer, db.ForeignKey("eo_project.projectID"))
    # 关系2
    project = db.relationship("EoProject", backref="apis")


# CREATE TABLE `eo_api_header` (
#   `headerID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `headerName` varchar(255) NOT NULL,
#   `headerValue` text NOT NULL,
#   `apiID` int(10) unsigned NOT NULL,
#   PRIMARY KEY (`headerID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8
# 🌟 14. 接口文档 - 请求头部表
'''
接口表 和 请求头部表 : 一对多关系
'''


class EoApiHeader(db.Model):
    __tablename__ = 'eo_api_header'

    headerID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 请求头ID
    headerName = db.Column(db.String(255), nullable=False)  # 请求头的名
    headerValue = db.Column(db.String(255), nullable=False)  # 请求头的值

    # 外键
    apiID = db.Column(db.Integer, db.ForeignKey("eo_api.apiID"))  # apiID
    # 关系
    api = db.relationship("EoApi", backref="headers")


# CREATE TABLE `eo_api_request_param` (
#   `paramID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `paramName` varchar(255) COLLATE utf8_bin DEFAULT NULL,
#   `paramKey` varchar(255) COLLATE utf8_bin NOT NULL,
#   `paramValue` text COLLATE utf8_bin NOT NULL,
#   `paramType` tinyint(3) unsigned NOT NULL DEFAULT '0',
#   `paramLimit` varchar(255) COLLATE utf8_bin DEFAULT NULL,
#   `apiID` int(10) unsigned NOT NULL,
#   `paramNotNull` tinyint(1) NOT NULL DEFAULT '0',
#   PRIMARY KEY (`paramID`),
#   KEY `apiID` (`apiID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
# 🌟 15. 接口 - 请求参数表
'''
接口表 和 请求参数表 : 一对多关系
'''


class EoApiRequestParam(db.Model):
    __tablename__ = 'eo_api_request_param'

    paramID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 参数ID
    paramName = db.Column(db.String(255), default=None)  # 说名
    paramKey = db.Column(db.String(255), nullable=False)  # 参数名
    paramValue = db.Column(db.Text, nullable=False)  # 参数示例
    paramType = db.Column(db.Boolean(3), default=0)  # 参数类型
    paramLimit = db.Column(db.String(255), default=None)  # 参数限制
    paramNotNull = db.Column(db.Boolean, nullable=False, default=0)  # 参数非空

    # 外键1 - apiID
    apiID = db.Column(db.Integer, db.ForeignKey("eo_api.apiID"))
    # 关系1
    api = db.relationship("EoApi", backref="request_params")


# CREATE TABLE `eo_api_request_value` (
#   `valueID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `value` text,
#   `valueDescription` varchar(255) DEFAULT NULL,
#   `paramID` int(10) unsigned NOT NULL,
#   PRIMARY KEY (`valueID`),
#   KEY `paramID` (`paramID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8
# 🌟 16. 接口 - 请求值表
'''
请求参数表 和 请求值表 : 一对一关系
'''


class EoApiRequestValue(db.Model):
    __tablename__ = 'eo_api_request_value'

    valueID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Text)

    # 外键1
    paramID = db.Column(db.Integer, db.ForeignKey('eo_api_request_param.paramID'))
    # 关系1
    param = db.relationship("EoApiRequestParam", backref=db.backref('request_value', uselist=False))


# CREATE TABLE `eo_api_result_param` (
#   `paramID` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `paramName` varchar(255) COLLATE utf8_bin DEFAULT NULL,
#   `paramKey` varchar(255) COLLATE utf8_bin NOT NULL,
#   `apiID` int(11) unsigned NOT NULL,
#   `paramNotNull` tinyint(1) unsigned NOT NULL,
#   PRIMARY KEY (`paramID`),
#   KEY `apiID` (`apiID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
# 🌟 16. 接口 - 返回参数表
'''
接口表 和 返回参数表 : 一对多关系
'''


class EoApiResultParam(db.Model):
    __tablename__ = 'eo_api_result_param'

    paramID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    paramName = db.Column(db.String(255), nullable=False, default=None)
    paramKey = db.Column(db.String(255), nullable=False, default=None)
    paramNotNull = db.Column(db.Boolean, nullable=False)

    # 外键
    apiID = db.Column(db.Integer, db.ForeignKey('eo_api.apiID'))
    # 关系
    api = db.relationship("EoApi", backref="result_params")


# CREATE TABLE `eo_api_result_value` (
#   `valueID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `value` text COLLATE utf8_bin NOT NULL,
#   `valueDescription` varchar(255) COLLATE utf8_bin DEFAULT NULL,
#   `paramID` int(10) unsigned NOT NULL,
#   PRIMARY KEY (`valueID`),
#   KEY `resultParamID` (`paramID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
# 🌟 17. 接口 - 返回值表
'''
接口返回参数表 和 返回值表 : 一对一关系
'''


class EoApiResultValue(db.Model):
    __tablename__ = 'eo_api_result_value'

    valueID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Text)
    valueDescription = db.Column(db.String(255), default=None)

    # 外键
    paramID = db.Column(db.Integer, db.ForeignKey("eo_api_result_param.paramID"))
    # 关系
    param = db.relationship("EoApiResultParam", backref=db.backref('result_value'), uselist=False)


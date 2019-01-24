#coding=utf-8

from rest_framework import permissions

from apps.user_operation.models import *

#     只要是普通用户就不允许访问，且超级管理员，管理员和专家没有区别  对应样本和物证的删除
# 都不能创建，因此创建的时候不能有这个权限限制
class IsAdmin(permissions.BasePermission):
    """
    只要是普通用户就不允许访问，且超级管理员，管理员和专家没有区别  对应样本和物证的删除
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.role ==3:
                return False
            else:
                return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.role ==3:
                return False
            else:
                return True

#对人员的操作
# 普通用户和专家都不能够对人员进行增加和删除等不安全的操作，管理员只能操作比他角色大，即普通用户和专家的操作，超级管理员可以操作所有的操作，包括他自己
class IsSuperAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            if request.user.role ==3:
                return False
            else:
                return True
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method not in permissions.SAFE_METHODS:
            if request.user.role == 3 or request.user.role == 4:
                return False
            elif request.user.role ==2:
                return obj.role > request.user.role
            else:
                return True
        return True

# 只有普通用户自己上传的才可以操作
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.role == 3:
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj.user == request.user
        return True

# 请求炸药核准的权限
class IsAllowExploUpdate(permissions.BasePermission):
    # 只有在更新时才会来验证这个权限，在是第三角色时如果请求不安全，即更新，则只能更新自己上传的物证的记录，即只能核准自己上传的物证的综合匹配记录
    # 不能用统一的权限类，因为查询这个物证的处理人是谁的时候需要两种：炸药和爆炸装置

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.role == 3:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                # 如果在allowUpdate表中存在记录也返回True，没有记录则返回False
                record = exploEvi.objects.get(id =obj.exploEvi.id)
                if record.user == request.user:
                    return True
                else :
                    return False
        return True

# 请求爆炸装置核准的权限类
class IsAllowDevUpdate(permissions.BasePermission):
    # 只有在更新时才会来验证这个权限，在是第三角色时如果请求不安全，即更新，则只能更新自己上传的物证的记录，即只能核准自己上传的物证的综合匹配记录
    # 不能用统一的权限类，因为查询这个物证的处理人是谁的时候需要两种：炸药和爆炸装置

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.role == 3:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                # 这里能不能加一个差错提醒，就是每个如果这个id在Evi表中找不到，返回请求核准的物证不在的错误

                # 如果在allowUpdate表中存在记录也返回True，没有记录则返回False
                record = devEvi.objects.filter(id =obj.devEvi.id)
                if record.user == request.user:
                    return True
                else :
                    return False
        return True

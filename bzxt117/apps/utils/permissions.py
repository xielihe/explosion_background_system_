#coding=utf-8

from rest_framework import permissions

from apps.user_operation.models import *


class IsAdmin(permissions.BasePermission):
    """
    只要是第三角色就不允许访问，且第一和第二角色没有区别  对应样本和物证的删除
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
            if request.user.role ==3:
                return False
            elif request.user.role ==2:
                return obj.role > request.user.role
            else:
                return True
        return True

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.role == 3:
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj.user == request.user
        return True


class IsAllowExploUpdate(permissions.BasePermission):
    # 只有在更新时才会来验证这个权限，在是第三角色时如果请求不安全，即更新，则如果在allowUpdate表中存在人员和物证对应的记录，则返回True，否则为False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.role == 3:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                # 如果在allowUpdate表中存在记录也返回True，没有记录则返回False
                records = allowUpdate.objects.filter(exploEviId=obj.exploEviId, entitled=request.user)
                if len(records) ==0 :
                    return False
        return True

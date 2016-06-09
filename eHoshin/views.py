from rest_framework import permissions
import sys

def is_team_owner(view):
    """Check if the user is the owner of the current team.

    Args:
        view: the view acceded by the user

    Returns:
        bool: True if he's the owner, False otherwise
    """
    return view.request.user.is_owner_of(view.kwargs['team'])


def is_team_moderator(view):
    """Check if the user is a moderator of the current team.

    Args:
        view: the view acceded by the user

    Returns:
        bool: True if he's a moderator, False otherwise
    """
    return view.request.user.is_moderator_of(view.kwargs['team']) or is_team_owner(view)


def is_team_member(view):
    """Check if the user is a member of the current team.

    Args:
        view: the view acceded by the user

    Returns:
        bool: True if he's a member, False otherwise
    """
    return view.request.user.is_member_of(view.kwargs['team'])


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or admins to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.object_ptr.owner == request.user or is_team_moderator(view)


class IsUser(permissions.BasePermission):
    """
    Object-level permission to only allow users of an object to access it.
    Assumes the model instance has an `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or is_team_moderator(view)


class IsMyselfOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow the user himself to see his profile the team owner.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user or is_team_owner(view)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return is_team_owner(view)


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow moderator to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return is_team_owner(view) or is_team_moderator(view)


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or the team owner to access it.
    Assumes the model instance has an `follower` attribute.
    """
    def has_object_permission(self, request, view, obj):
        return obj.follower == request.user or is_team_owner(view)


class IsMember(permissions.BasePermission):
    """
    Object-level permission to only allow member of the team which belonging to the object  to access it.
    """
    def has_object_permission(self, request, view, obj):
        return is_team_member(view)

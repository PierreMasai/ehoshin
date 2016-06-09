"""Some general auxiliary functions shared by all the applications."""
from django.core.exceptions import PermissionDenied


def check_user_permission(user, team):
    """Check the access right of an user to a team.

    Args:
        user (User): The user of whom the permission is checked.
        team (Team): The team to verify.

    Raises:
        PermissionDenied: If the user has not the permission.
    """
    if not user.is_member_of(team):
        raise PermissionDenied


class Http403(Exception):
    """The 403 error exception."""
    pass

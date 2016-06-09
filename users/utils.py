"""Some general auxiliary functions used in the other users modules."""

from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth

from . import models


def login_user(request, user):
    """Log in the user and add it to the request.

    Args:
        request: The overall context.
        user (dict): The user to log in.
    """
    auth.login(request, user)

    tokens = Token.objects.filter(user=user)

    if tokens:
        Token.objects.filter(user=request.user).delete()

    token = Token.objects.create(user=user)
    token.save()

    request.session['token'] = token.key


def logout_user(request):
    """Log out the user.

    Args:
        request: The context.
    """
    tokens = Token.objects.filter(user=request.user)
    tokens.delete()

    auth.logout(request)


def get_user_from_full_name(full_name):
    """
    Return a user, or None if there is not/many of them
    Args:
        full_name: the full name of the user

    Returns:
        User model or None
    """
    first_name = ''
    last_name = ''
    if full_name:
        names = full_name.split(" ")
        first_name = names[0]
        last_name = ' '.join(names[1:])

    try:
        return models.User.objects.get(first_name=first_name, last_name=last_name)
    except ObjectDoesNotExist:
        return None

# -*- coding: utf-8 -*-

from django.shortcuts import render
from hoshins.utils import *
import os.path
from django.http import HttpResponse
from . import models, excel_utils, rest_views
import sys


def format_object_type_name(name):
    """Format the ``name``.

    Convert the ``name`` into camelcase and put it in
    singular.
    Args:
        name (str): the name to convert.

    Returns:
        str: the name converted.
    """
    name = to_camelcase(name)
    name = name[0].upper() + name[1:]

    if name[-3:] == 'ies':
        return name[:-3] + 'y'
    else:
        return name[:-1]


def get_rest_view_class(name, is_detail):
    """Get a rest view class from his name.

    The rest view is picked up among the class in the
    rest_views module belonging to the current one.
    Args:
        name (str): name of the view to get.
        is_detail (bool): type of the view. True means
            detail type and False list type.

    Returns:
        class: return the view class
    """
    if is_detail:
        name += 'Detail'
    else:
        name += 'List'

    return getattr(sys.modules['hoshins.rest_views'], name)


def get_rest_view(object_type, is_detail=False):
    """Get a rest view.

    Args:
        object_type (str): the type of the object we want to get.
        is_detail (bool): define the type of the class returned
            (single object or list)

    Returns:
        View: the view
    """
    object_type = format_object_type_name(object_type)
    rest_view = get_rest_view_class(object_type, is_detail)
    return rest_view.as_view()


def rest_api_detail(request, name, object_type, **kwargs):
    """Give access to a model rest view.

    Args:
        request: the context.
        name (str): the name of the team.
        object_type (str): the type of the object/model we want.
        **kwargs (dict): some attributes to give to the view.

    Returns:
        View: return the view according to the object type.
    """
    kwargs['team'] = name
    rest_view = get_rest_view(object_type, True)
    return rest_view(request, **kwargs)


def rest_api_list(request, name, object_type, **kwargs):
    """Give access to a model list rest view.

    Args:
        request: the context.
        name (str): the name of the team.
        object_type (str): the type of the object/model we want.
        **kwargs (dict): some attributes to give to the view.

    Returns:
        View: return the view according to the object type.
    """
    kwargs['team'] = name
    rest_view = get_rest_view(object_type)
    return rest_view(request, **kwargs)


def get_leader_synthesis(request, pk):
    """Give the items synthesis for a leader with an excel file.

    Args:
        request: the context.

    Returns:
        HttpResponse: The excel file containing the abstract..
    """
    items = models.Item.objects.filter(parent__id=pk)
    if not request.GET.get('items', None) == 'all':
        items = items.filter(leader=request.user.full_name)

    excel_file = excel_utils.leader_to_excel(items)
    response = HttpResponse(excel_file.read(), content_type='application/excel')
    response['Content-Disposition'] = 'inline; filename=themes_synthesis.xlsx'
    return response


def get_hoshin_synthesis(request, pk):
    """Give the hoshin synthesis for a member with an excel file.

    Args:
        request: the context.
        pk (int): the id of the hoshin.
    Returns:
        HttpResponse: The excel file containing the abstract..
    """
    excel_file, hoshin_name = excel_utils.statistics_to_excel(pk)
    response = HttpResponse(excel_file.read(), content_type='application/excel')
    response['Content-Disposition'] = 'inline; filename='+hoshin_name
    return response


def add_user_information(request, team_name):
    """Add user information upton to the request.

    This function will add the type of relation that the user has
    with the team to his model in the request.

    Args:
        request: the context to enrich.
        team_name (str): the name of the current team
    """
    request.user.is_owner = request.user.is_owner_of(team_name)
    if request.user.is_owner:
        request.user.is_moderator = True
    else:
        request.user.is_moderator = request.user.is_moderator_of(team_name)

    request.user.is_member = request.user.is_member_of(team_name)


def get_reference(request, team_name, ref_name):
    """Get a reference document.

    Args:
        request: the context.
        team_name (str): the name of the team to which the reference is belonging.
        ref_name (str): the name of the reference we want to get.

    Returns:
        HttpResponse: The reference document.
    """
    ref_name += '.pdf'
    path = ['ressources', team_name, 'references', ref_name]
    path = '/'.join(path)

    if not os.path.isfile(path):
        return render(request, 'hoshins/unknown_reference.html', status=404)

    with open(path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename='+ref_name
        return response

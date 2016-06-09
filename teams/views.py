# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from hoshins.utils import *
from django.http import Http404
import os.path
from django.http import HttpResponse
from . import models, utils
from django.conf import settings
from eHoshin.utils import Http403
import users
import hoshins
from .forms import TeamForm
import re


def create_or_join_team(request, name):
    """Create or join a team.

    Args:
        request: the context.
        name (str): the name of the team

    Returns:
        HttpResponse: the response to give back to the user.
    """
    if not utils.verify_team_name(name):
        to_return = render(request, 'hoshins/home.html', {
                   'error': 'This name isn\'t authorize, let\'s try another'
               })
    elif not re.match(r'^[A-Za-z0-9_]+$', name):
        to_return = render(request, 'hoshins/home.html', {
                    'error': 'The name must be composed with alphanumeric characters and underscores'
                })
    elif request.user.is_member_of(name):
        to_return = HttpResponseRedirect('/' + name)
    else:
        try:
            team = models.Team.objects.get(name=name)
            if team.is_closed:
                to_return = render(request, 'hoshins/home.html', {
                    'error': 'This organisation is closed, you can\'t join it'
                })
            elif team.is_private:
                to_return = render(request, 'hoshins/home.html', {
                    'error': 'This organisation is private, you can\'t join it'
                })
            else:
                full_name = request.user.full_name
                items = hoshins.models.Item.objects.filter(object_ptr__belongs_to=team)
                membership_type = users.models.Membership.NORMAL_USER

                for item in items:
                    if item.leader == full_name:
                        membership_type = users.models.Membership.MODERATOR
                        break

                users.models.Membership.objects.get_or_create(member=request.user, team=team,
                                                              type=membership_type)

                hos = hoshins.models.Hoshin.objects.filter(object_ptr__belongs_to=team)
                for ho in hos:
                    ho.nb_users += 1
                    ho.save()
                    
                to_return = HttpResponseRedirect('/' + name)

        except ObjectDoesNotExist:
            team = models.Team.objects.create(name=name)
            team.save()
            m = users.models.Membership.objects.create(member=request.user, team=team,
                                                       type=users.models.Membership.OWNER)
            m.save()

            to_return = HttpResponseRedirect('/' + name)

    return to_return


def home(request):
    """The home view.

    This view hold the main page of the web site, called with
    the root url.
    Args:
        request: the context

    Returns:
        HttpResponse: the main page response.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login?next=' + request.path)

    elif request.user.member_of.exists():
        return HttpResponseRedirect('/' + request.user.member_of.first().name)
    if request.POST and request.POST['name']:
        name = request.POST['name']
        return create_or_join_team(request, name)
    else:
        return render(request, 'hoshins/home.html', {'canSignup': settings.CAN_SIGNUP})


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


def team_home(request, name):
    """View of the team's main page.

    Args:
        request: the context
        name (str): the name of the team

    Returns:
        HttpResponse: The main page of the team, or an error one
            if something gone wrong (unknown team, unauthorized access)
    """
    response = HttpResponseRedirect('/accounts/login?next=' + request.path)

    if request.user.is_authenticated():
        try:
            team = models.Team.objects.get(name=name)
        except ObjectDoesNotExist:
            response = render(request, 'hoshins/unknown_home.html', {'team_name': name}, status=404)
        else:
            add_user_information(request, name)

            if request.user.is_member:
                is_leader = hoshins.models.Item.objects.filter(object_ptr__belongs_to__name=name)\
                    .filter(leader=request.user.full_name).exists()

                response = render(request, 'hoshins/team_home.html', {
                    'team_name': name,
                    'references': team.references,
                    'is_leader': is_leader,
                })
            else:
                response = render(request, 'hoshins/unauthorized_home.html', {'team_name': name}, status=403)

    return response


def connect_team_settings(request, name):
    """Check the authorization for the team settings access.

    Args:
        request: the context
        name (str): the name of the team

    Raises:
        Http403: An unauthorized access.

    Returns:
        dict: return the team
    """
    if request.user.is_authenticated():
        team = get_object_or_404(models.Team, name=name)

        add_user_information(request, name)
        if request.user.is_owner_of(name) or request.user.is_moderator_of(name):
            return team

    raise Http403


def get_settings_render(request, name, page_url, options={}):
    """Get the render to a team settings access.

    Display the setting page we want to get, or an
    error one if something gone wrong.

    Args:
        options (dict): Options to add to the render
        request: the context
        name (str): the name of the team
        page_url (str): the setting url we want to access

    Returns:
        HttpResponse: the setting page to display, or an
            error one.
    """
    options['team_name'] = name
    try:
        team = connect_team_settings(request, name)
        options['team'] = team
    except Http404:
        return render(request, 'hoshins/unknown_home.html', options, status=404)
    except Http403:
        return render(request, 'hoshins/unauthorized_home.html', options, status=403)
    else:
        return render(request, page_url, options)


def basic_settings(request, name):
    """Basic setting page.

    Args:
        request: the context.
        name (str): the name of the team.

    Returns:
        HttpResponse: the basic setting page.
    """
    if request.POST:
        request.POST._mutable = True
        request.POST['is_private'] = 'is_private' in request.POST
        request.POST['is_closed'] = 'is_closed' in request.POST
        request.POST._mutable = False

    instance = get_object_or_404(models.Team, name=name)
    form = TeamForm(request.POST or None, instance=instance)
    message = None

    if form.is_valid():
        new_instance = form.save()
        new_instance.save()
        message = "The settings has been updated"

        if new_instance.name != name:
            return HttpResponseRedirect('/'.join(['', new_instance.name, 'settings', 'basics']))

    return render(request, 'teams/basics.html', {
        'message': message,
        'team_name': name,
        'form': form
    })


def dashboard_settings(request, name):
    """Basic setting page.

    Args:
        request: the context.
        name (str): the name of the team.

    Returns:
        HttpResponse: the basic setting page.
    """
    return get_settings_render(request, name,
                               'teams/dashboard.html')


def users_settings(request, name):
    """User setting page.

    Args:
        request: the context.
        name (str): the name of the team.

    Returns:
        HttpResponse: the user setting page.
    """
    return get_settings_render(request, name,
                               'teams/user.html')

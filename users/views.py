# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.template import RequestContext
from django.http import HttpResponse
from . import forms, utils
from django.conf import settings


def authenticate_user(request, username, password):
    """Authenticate the user.

    The function give an error message if a problem happen
    during the authentication.

    Args:
        request: the context.
        username (str): the username of the user to authenticate.
        password (str): his password.

    Returns:
        bool, optional[str]: True if the authentication goes right,
            False otherwise with an error message
    """
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            utils.login_user(request, user)
            return True, None
        else:
            return False, 'Account disabled'
    else:
        return False, 'The password or the username you’ve entered is incorrect. \
                           Please re-enter them.'


def get_redirection_url(request):
    redirection_url_default = '/'
    try:
        redirection_url = request.GET.get('next', redirection_url_default)
        redirection_url = str(redirection_url)
    except:
        redirection_url = redirection_url_default

    return redirection_url


def login(request):
    """The basic login view.

    This view let the user to log in and redirect it toward
    the ``next`` attribute if given, the root page otherwise.
    It can be overwritten to adapt it to a company.
    Args:
        request: the context.

    Returns:
        HttpResponse: the response to give back to the user.
    """
    redirection_url = get_redirection_url(request)

    if request.user.is_authenticated():
        return HttpResponseRedirect(redirection_url)
    else:
        params = {
            'next': redirection_url,
            'canSignup': settings.CAN_SIGNUP
        }

        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            result, errors = authenticate_user(request, username, password)
            if result:
                return HttpResponseRedirect(redirection_url)
            else:
                params['error'] = errors

        return render_to_response('users/login.html', params,
                                  RequestContext(request))


def logout(request):
    """The basic logout view.

    This view let the user to log ou and redirect it on the
    root page of the website..
    Args:
        request: the context.

    Returns:
        HttpResponse: the response to give back to the user.
    """
    utils.logout_user(request)

    return HttpResponseRedirect('/')


def signup(request):
    """The basic signup view.

    This view let the user to signup and redirect it toward
    the ``next`` attribute if given, the root page otherwise.
    It can be overwritten to adapt it to a company.
    Args:
        request: the context.

    Returns:
        HttpResponse: the response to give back to the user.
    """
    redirection_url = get_redirection_url(request)

    if request.user.is_authenticated():
        return HttpResponseRedirect(redirection_url)

    if request.method == 'POST':
        uf = forms.UserForm(request.POST, prefix='user')
        if uf.is_valid():
            uf.save()
            authenticate_user(request, uf.cleaned_data['username'],
                              uf.cleaned_data['password'])

            return HttpResponseRedirect(redirection_url)
    else:
        uf = forms.UserForm(prefix='user')

    return render_to_response('users/signup.html',
                              {
                                  'form': uf,
                                  'next': redirection_url,
                                  'canSignup': settings.CAN_SIGNUP
                              },
                              context_instance=RequestContext(request))


def user_view(request):
    """The user profile view.

    This view is called when the user want to update his profile.
    Args:
        request: the context

    Returns:
        HttpResponse: the response to give back to the user.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login?next=' + request.path)

    message = None
    profile_form = forms.ProfileForm('profile' in request.POST and request.POST or None,
                                     prefix='profile', instance=request.user)
    password_form = forms.PasswordForm('password' in request.POST and request.POST or None,
                                       prefix='password', instance=request.user)

    if profile_form.is_valid():
        profile_form.save()
        message = "Your profile has been updated"
    if password_form.is_valid():
        password_form.save()
        message = "Your password has been updated"
        authenticate_user(request, request.user.username,
                          password_form.cleaned_data['new1'])

        password_form = forms.PasswordForm(prefix='password', instance=request.user)

    return render_to_response('users/settings.html',
                              {
                                  'message': message,
                                  'profile_form': profile_form,
                                  'password_form': password_form
                              },
                              context_instance=RequestContext(request))

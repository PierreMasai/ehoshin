"""Some general auxiliary functions used in the other hoshin modules."""
from rest_framework.response import Response
from rest_framework.exceptions import status
from notifications.models import notify
from django.core.exceptions import ObjectDoesNotExist
import re
import os

from eHoshin.utils import check_user_permission
from django.contrib.auth.models import User


def to_camelcase(s):
    """Convert the string in camel case.
    Args:
        s (str): The string to convert

    Returns:
        str: The string converted.
    """
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)


def verify_team_name(name):
    """ Verify the name of the team

    Args:
        name (str): THe name of the team

    Returns:
        bool: True if the name is not in the blacklist,
            False otherwise.
    """

    blacklist = ['accounts', 'admin', 'teams',
                 'toyota_auth', 'login_toyota']

    blackones = [elt for elt in blacklist if name in elt]

    return not blackones


def get_team_elements(user, team, model):
    """Get a query with all the elements of the ``model`` type of a team.

    Args:
        user (User): The user who want to get the elements.
        team (Team): The team of which we want the elements
        model: The type of elements we want to get

    Returns:
        Query: the query to get the elements belonging to the team
    """
    check_user_permission(user, team)
    return model.objects.filter(object_ptr__belongs_to__name=team)


def get_personal_comments(user, team, filtered):
    """Get the comment of the ``user`` in the previous query.

    Args:
        user (User): The current user
        team (Team): The current team
        filtered (Query): The query to precise

    Returns:
        Query: The query with only the comment from the ``user``.
    """
    if not user.is_moderator_of(team):
        check_user_permission(user, team)
        return filtered.filter(object_ptr__owner=user)
    else:
        return filtered


def get_flatten_fields(fields):
    """Get the flatten fields.

    The nested object are flatten, then added to the fields list.
    Args:
        fields (dict): fields to flatten

    Returns:
        dict: The previous dictionary with the flatten nested fields.
    """
    flatten_fields = {}

    for field_name, field in fields.items():
        if getattr(field, 'flatten', False):
            for nested_field_name, nested_field in field.fields.items():
                nested_field.source = (field_name + '.' +
                                       (nested_field.source or nested_field_name))
                flatten_fields[nested_field_name] = nested_field
        else:
            flatten_fields[field_name] = field

    return flatten_fields


def create_model(view, request, *args, **kwargs):
    """Auxiliary function to create a model from a serializer of the view.

    Args:
        view (View): The view of which we use the serializer
        request: The overall information
        *args:
        **kwargs:

    Returns:
        dict: Return the instance of the model created
    """
    serializer = view.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    view.perform_create(serializer)

    return serializer.data


def create_response(view, data):
    """Create an Http response from the data if the serializer was valid.

    Args:
        view (View): The view which call this function
        data (data): The data to put in the answer

    Returns:
        HttpResponse: The response to send back to the user
    """
    headers = view.get_success_headers(data)
    return Response(data, status=status.HTTP_201_CREATED, headers=headers)


def get_hoshin(model):
    """Get the hoshin of the model given.

    Args:
        model: The model of which we want to get the hoshin.

    Returns:
        Hoshin: The hoshin of which the model is belonging
    """
    if hasattr(model, 'parent'):
        model = get_hoshin(model.parent)
    if hasattr(model, 'item'):
        model = get_hoshin(model.item)
    elif hasattr(model, 'implementationpriority'):
        model = get_hoshin(model.implementationpriority)

    if hasattr(model, 'hoshin'):
        model = model.hoshin

    return model


def get_infos_to_notify(model):
    """
    This function get the information needed to create a notification
    it's composed by the url of the object notified (to permit the user to reach it)
    and the follower of the item (the person to notify)
    Args:
        model: A model (Hoshin, Item or a Priority)

    Returns:
        A tuple (list, list): The follower list and the path of the object
    """
    users_list = []
    path = []
    if model:
        core = model.object_ptr
        followers = core.followed_by.all()

        if hasattr(model, 'parent'):
            users_list, path = get_infos_to_notify(model.parent)

        path = path + [str(core.global_id)]
        users_list += [elt.follower for elt in followers if elt.follower not in users_list]

    return users_list, path


def get_model_infos(model, team_name):
    """
    This function get the url of a model (used for the notification)
    Args:
        team_name (str): The name of the team
        model: A model (Hoshin, Item or a Priority)

    Returns:
        str: The path of the object
        str: The model type
        model: Instance of the model
    """
    path = []
    current_model = model
    model_type = None
    if model:
        if hasattr(model, 'item'):
            current_model = model.item
            model_type = 'item'
        elif hasattr(model, 'hoshin'):
            current_model = model.hoshin
            model_type = 'hoshin'
        else:
            current_model = model.implementationpriority
            model_type = 'concrete action'

        path.insert(0, str(current_model.id))
        model = current_model
        while hasattr(model, 'parent'):
            model = model.parent
            path.insert(0, str(model.id))

    return os.sep + os.path.join('', team_name, *path), model_type, current_model


def notify_followers(model, actor, text):
    """
    The function create a notification for all the person who need it.
    Meaning, all the follower but not the one who made the action

    Args:
        model: the subject of the notification
        actor: the user who did the action
        text: the text to show in the notification
    """
    users_to_notify, path = get_infos_to_notify(model)

    # -1 to get the path of his parent
    path = '/' + '/'.join(path[:-1])

    if actor in users_to_notify:
        users_to_notify.remove(actor)

    for user in users_to_notify:
        notify.send(user, recipient=user, verb=text, url=path)


def notify_action(model, action_name, recipient=None):
    """
    Notify the followers about any action on an object
    Args:
        model: the subject to notify
        action_name: the type of action
        recipient: the one who did the action
    """
    obj = model.object_ptr
    if not recipient:
        recipient = obj.owner

    name = model.get_trunc_name()

    notify_followers(model, recipient, "<strong>" + recipient.full_name + "</strong>" +
                     action_name + "<strong>" + name + "</strong>")


def get_author(model):
    """Get the user who wrote the comment.

    Args:
        model (Comment): The comment of which we want to get the author.

    Returns:
        optional[User]: The author if we found it, None otherwise
    """
    core = model.object_ptr
    if core.owner_temp == "" and core.owner:
        author = core.owner
    else:
        try:
            full_name = core.owner_temp.split(' ')
            author = User.objects.get(first_name=full_name[0], last_name=' '.join(full_name[1:]))
        except ObjectDoesNotExist:
            author = None

    return author


def notify_comment(comment, team_name):
    """Send a notification when a comment is wrote.

    Args:
        comment (Comment): The comment wrote
        team_name (str): the name of the team in which the user wrote.
    """
    target = comment.parent
    comments_query = target.comments
    authors = []
    url, model_type, target = get_model_infos(target, team_name)
    url = os.path.join(url, 'comments')

    for comment in comments_query.all():
        author = get_author(comment)
        if author and author not in authors:
            authors.append(author)

    current_author = get_author(comment)
    if current_author in authors:
        authors.remove(current_author)

    for author in authors:
        old_notifications = author.notifications.unread()
        last_read = author.notifications.read()[0]
        old_notifications = [elt for elt in old_notifications if elt.target == target]

        if old_notifications and old_notifications[0].timestamp > last_read.timestamp:
            old_notif = old_notifications[0]
            old_notif.data['nb'] += 1
            old_notif.verb = "<strong>" + str(old_notif.data['nb']) + \
                             "</strong> comments were added to the " + model_type + " <strong>" + \
                             old_notif.target.get_trunc_name() + "</strong>"
            old_notif.save()
        else:
            text = "<strong>" + author.full_name + "</strong> added a comment to the " + \
                   model_type + " <strong>" + target.get_trunc_name() + "</strong>"

            notify.send(author, recipient=current_author, target=target, verb=text, url=url, nb=1)

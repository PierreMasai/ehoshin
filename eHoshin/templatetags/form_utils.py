from django import template
from django.forms.widgets import CheckboxInput
register = template.Library()


@register.filter
def field_type(field):
    """Get the name of the field class.

    Args:
        field: the field fo the form

    Returns:
        str: the name of the field type (of the subfield if it's in the types list)
    """
    types = ['password', 'email', 'username']

    for t in types:
        if t in field.html_name:
            return t

    if hasattr(field, 'field'):
        field = field.field

    s = str(type(field.widget).__name__)
    s = s.rpartition('Input')[0]
    s = s.lower()

    return s


@register.filter
def is_checked(field):
    """Get the name of the field class.

    Args:
        field: the field fo the form

    Returns:
        str: the name of the field type (of the subfield if it's in the types list)
    """
    value = field.value()
    if hasattr(field, 'field'):
        field = field.field

    if isinstance(field.widget, CheckboxInput):
        if value:
            return "checked"

    return False


@register.filter
def to_string(value):
    """Return a string form an optional string.

    Args:
        value(Optional[str]): the string value

    Returns:
        str: value if it's a string, and and empty string if the value is None
    """
    return value and str(value) or ""


@register.filter
def is_autocompleted(field):
    """Check if the field has to be auto-completed.
    Args:
        field: the field to check

    Returns:
        str: return 'on' if the field has to be auto-completed,
            'off' otherwise.
    """
    return field_type(field) == 'password' and 'off' or 'on'


@register.filter
def is_moderator(user, team):
    """Check if the user is a moderator of the team.

    This function is used to display the user list. If it's a moderator, the radiobox
    will be checked, and not checked otherwise.

    Args:
        user (model): The current user
        team (model): The current team

    Returns:
        str: 'checked' if the user is a moderator, '' otherwise
    """
    return (user.is_moderator_of(team.name)) and 'checked' or ''

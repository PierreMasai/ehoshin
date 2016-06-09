from django.template import Library

register = Library()


@register.filter
def names(l):
    """Get the name of all the elements of the list.

    Assumes the elements have an `name` attribute.
    Args:
        l (list): a list of elements.

    Returns:
        list: the list of names.
    """
    return [elt.name for elt in l]

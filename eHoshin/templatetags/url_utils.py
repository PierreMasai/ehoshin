from django import template

register = template.Library()


@register.filter
def url_root(path):
    """Get the root of the url.
    Args:
        path (str): The url to get the root.

    Returns:
        str: The root of the url if it exists, an empty string otherwise.
    """
    return path and '/' + path.split('/')[1] or ''


@register.filter
def url_add(path, argument):
    """Construct an url by adding an argument to the path.

    Args:
        path (str): The current path.
        argument (str): The string to add to have the subpath.

    Returns:
        str: Return the full path.
    """
    return path + '/' + argument

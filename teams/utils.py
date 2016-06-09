"""Some general auxiliary functions used in the other teams modules."""


def verify_team_name(name):
    """ Verify the name of the team

    Args:
        name (str): THe name of the team

    Returns:
        bool: True if the name is not in the blacklist,
            False otherwise.
    """

    blacklist = ['accounts', 'admin', 'teams']

    blackones = [elt for elt in blacklist if name in elt]

    return not blackones

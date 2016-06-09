from django.db import models
from django.contrib.auth.models import User
from teams.models import Team


###########
# basics functions
###########


def update_instance(instance, data, commit=True):
    """The function update a db object.

    Args:
        commit (bool): True to save the modification, False otherwise
        instance: A db object to update.
        data (dict): A dictionary with all the attributes to change .

    Returns:
        The instance updated.
    """
    for (key, value) in data.items():
        setattr(instance, key, value)

    if commit:
        instance.save()

    return instance


###########
# models
###########

class Membership(models.Model):
    """This model own the membership information."""
    member = models.ForeignKey(User)
    team = models.ForeignKey(Team)

    NORMAL_USER = 'NO'
    MODERATOR = 'MO'
    OWNER = 'OW'
    NOT_A_MEMBER = 'NM'

    TYPES = (
                (OWNER,         'Owner'),
                (MODERATOR,     'Moderator'),
                (NORMAL_USER,   'Normal user'),
                (NOT_A_MEMBER,  'Not a member')
             )

    type = models.CharField(max_length=2, choices=TYPES, default=NORMAL_USER)


# The following auxiliary functions are added to the user model to ease
# the access to the membership type.

def is_member_of(self, team_name):
    """Check if the current user is a member of the team.

    Args:
        self (User): The user model
        team_name (str): The name of the team (which is unique)

    Returns:
        bool: True if the user is a member of the team, False otherwise
    """
    return self.member_of.filter(name=team_name).exists()


def is_owner_of(self, team_name):
    """Check if the current user is  the iwner of the team.

    Args:
        self (User): The user model
        team_name (str): The name of the team (which is unique)

    Returns:
        bool: True if the user is the owner of the team, False otherwise
    """
    return self.member_of.filter(name=team_name,
                                 membership__type=Membership.OWNER).exists()


def is_moderator_of(self, team_name):
    """Check if the current user is a moderator of the team.

    Args:
        self (User): The user model
        team_name (str): The name of the team (which is unique)

    Returns:
        bool: True if the user is a moderator of the team, False otherwise
    """
    return self.member_of.filter(name=team_name,
                                 membership__type=Membership.MODERATOR).exists()


def is_normal_user_of(self, team_name):
    """Check if the current user is a normal user of the team.

    A normal user is neither the owner nor a administrator.

    Args:
        self (User): The user model
        team_name (str): The name of the team (which is unique)

    Returns:
        bool: True if the user is a normal user of the team, False otherwise
    """
    return self.member_of.filter(name=team_name,
                                 membership__type=Membership.NORMAL_USER).exists()


def full_name(self):
    """Wrapper to get the full name as a dynamic attribute (property).

    Args:
        self (User): The user model

    Returns:
        str: Return the full name of the user.
    """
    return self.get_full_name()


# The auxiliary functions are bind to the User model

User.full_name = property(full_name)
User.is_member_of = is_member_of
User.is_owner_of = is_owner_of
User.is_moderator_of = is_moderator_of
User.is_actor_of = is_normal_user_of

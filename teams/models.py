from django.db import models
from django.contrib.auth.models import User
import users


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


class Team(models.Model):
    """The team model.

    It's made up of a name, some attribute and a member list.
    """
    name = models.CharField(max_length=50, null=False)  # TODO: To set unique (handle serializer validator)
    members = models.ManyToManyField(User, related_name='member_of', through='users.Membership')

    is_private = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

"""Serializer module.

This module is used as a step between the model and the Rest part.
It aim to serialize the objects before sending them to the user,
as well as to recreate the models from the serialized data.

"""
from rest_framework import serializers
from . import models
import users


class TeamMinimalSerializer(serializers.ModelSerializer):
    """Get the team's name."""
    class Meta:
        model = models.Team
        fields = (
                    'name',
                 )


class TeamSerializer(serializers.ModelSerializer):
    """A complete team serializer."""
    references = users.serializers.UserMembershipSerializer(many=True, source='usermembership_set', required=False, read_only=True)

    class Meta:
        model = models.Team

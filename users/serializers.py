"""Serializer module.

This module is used as a step between the model and the Rest part.
It aim to serialize the objects before sending them to the user,
as well as to recreate the models from the serialized data.

"""
from rest_framework import serializers
from . import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import hoshins


class UserSerializer(serializers.ModelSerializer):
    """Serialize all the User model except the password field."""
    class Meta:
        model = models.User
        exclude = ('password',)


class UserMinimalSerializer(serializers.ModelSerializer):
    """Serialize the main user attributes."""
    class Meta:
        model = models.User
        fields = (
                    'id',
                    'username',
                    'first_name',
                    'last_name',
                 )
        extra_kwargs = {
            'username': {'validators': []},
        }


class MemberShipSerializer(serializers.ModelSerializer):
    """Serialize the membership model."""
    member = UserMinimalSerializer(read_only=True)
    type = serializers.CharField()

    class Meta:
        model = models.Membership
        fields = ('type', 'id', 'member')

    def create(self, validated_data):
        """Create the instance form the serializer.

        Args:
            validated_data (dict): The verified data.

        Returns:
            Returns the instance crated.
        """
        data = self.context['view'].request.data
        username = data['member']['username']
        try:
            validated_data['member'] = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            try:
                full_name = username.split(' ')
                validated_data['member'] = models.User.objects.get(first_name=full_name[0],
                                                                   last_name=' '.join(full_name[1:]))
            except models.User.DoesNotExist:
                raise Http404("User does not exist")

        kwargs = self.context['view'].kwargs
        team = kwargs['team']
        try:
            validated_data['team'] = hoshins.models.Team.objects.get(name=team)
        except models.User.DoesNotExist:
            raise Http404("Team does not exist")

        model_query = models.Membership.objects.filter(member=validated_data['member'],
                                                       team=validated_data['team'])
        if model_query.exists():
            return model_query.first()
        else:
            return self.Meta.model.objects.create(**validated_data)


class UserMembershipSerializer(serializers.ModelSerializer):
    """Serialize an user as well as his membership."""
    member_type = serializers.SerializerMethodField()

    def get_member_type(self, obj):
        """Function bound to the member_type attribute.

        This function is used to get the membership type of the member
        for the team present in the kwargs.

        Args:
            obj: The current instance of the member.

        Returns:
            Returns the type of the membership if it exists,
                NOT_A_MEMBER otherwise.
        """
        try:
            kwargs = self.context['view'].kwargs
            if 'team' in kwargs:
                team = models.Team.objects.get(name=kwargs['team'])
                ms = models.Membership.objects.get(member=obj, team=team)
                return ms.type

        except ObjectDoesNotExist:
            pass

        return models.Membership.NOT_A_MEMBER

    class Meta:
        model = models.User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'last_login',
            'date_joined',
            'member_type',
         )

    def update(self, instance, validated_data):
        """Update the user instance.

        Update or create the membership relation between the
        user instance and the current team.

        Args:
            instance (User): The user instance.
            validated_data (dict): The updated attributes,

        Returns:
            User: Return the user instance.
        """
        kwargs = self.context['view'].kwargs
        data = self.context['view'].request.data

        if 'team' in kwargs:
            team = models.Team.objects.get(name=kwargs['team'])
            member_type = data.pop('member_type', models.Membership.NORMAL_USER)

            if member_type not in [x[0] for x in models.Membership.TYPES]:
                member_type = models.Membership.NORMAL_USER

            ms, _ = models.Membership.objects.get_or_create(member=instance, team=team)
            ms.type = member_type
            ms.save()

        return super().update(instance, validated_data)

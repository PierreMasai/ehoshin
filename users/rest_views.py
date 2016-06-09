"""Module containing the rest related views

- *Filter: a class to held the different possibilities of filtering a request.
- *List: a view for listing models or creating a model instance.
- *Detail: a view for retrieving, updating or deleting a model instance.
"""
from rest_framework import generics, filters
from eHoshin.views import IsAdminOrReadOnly, IsModeratorOrReadOnly

from django.shortcuts import get_object_or_404
from . import serializers, models
from hoshins import utils


class MembershipList(generics.ListCreateAPIView):
    """Membership view for listing a queryset or creating a model instance."""
    queryset = models.Membership.objects.all()
    serializer_class = serializers.MemberShipSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        """
        This view should return a list of all user
        with a first name and a last name.
        """

        team_name = self.kwargs['team']
        utils.check_user_permission(self.request.user, team_name)
        team = get_object_or_404(models.Team, name=team_name)

        return team.membership_set


class MembershipDetail(generics.RetrieveUpdateDestroyAPIView):
    """Membership view for retrieving, updating or deleting a model instance."""
    queryset = models.User.objects.all()
    serializer_class = serializers.MemberShipSerializer
    permission_classes = (IsModeratorOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all user
        with a first name and a last name.
        """

        team_name = self.kwargs['team']
        utils.check_user_permission(self.request.user, team_name)
        team = get_object_or_404(models.Team, name=team_name)

        return team.membership_set


class UserList(generics.ListCreateAPIView):
    """User view for listing a queryset or creating a model instance."""
    queryset = models.User.objects.all()
    serializer_class = serializers.UserMembershipSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('first_name', 'last_name')
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all user
        with a first name and a last name.
        """

        if 'team' in self.request.GET:
            team_name = self.request.GET['team']
            utils.check_user_permission(self.request.user, team_name)
            team = get_object_or_404(models.Team, name=team_name)

            return team.members
        else:
            return self.queryset


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """User view for retrieving, updating or deleting a model instance."""
    queryset = models.User.objects.all()
    serializer_class = serializers.UserMembershipSerializer
    permission_classes = (IsModeratorOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all user
        with a first name and a last name.
        """

        if 'team' in self.request.GET:
            team_name = self.request.GET['team']
            utils.check_user_permission(self.request.user, team_name)
            team = get_object_or_404(models.Team, name=team_name)

            return team.members
        else:
            return self.queryset
